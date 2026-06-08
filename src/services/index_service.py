"""
Manages the FAISS vector index and a single atomic state file.

State file layout (pickle):
  {
    "file_hashes":  dict[str, str],   # {filename: sha256}
    "chunks":       list[dict],       # serialised Chunk objects
    "faiss_index":  bytes,            # faiss.serialize_index output
  }

The state file is written atomically (write-to-tmp → rename) so a crash
during rebuild never leaves a corrupted cache.

CQRS hook: this class is a pure state-holder/repository. Commands
(BuildIndexHandler) call build_or_load(); queries (AnswerQueryHandler)
call search(). Neither handler needs to know about FAISS internals.
"""

from __future__ import annotations

import os
import pickle
import tempfile
from dataclasses import asdict
from pathlib import Path

import faiss
import numpy as np

from src.services.document_loader_service import DocumentLoader
from src.services.embedding_service import EmbeddingService
from src.types import Chunk
from src.utils import DEFAULT_STATE_FILE


class IndexService:
    def __init__(
        self,
        loader: DocumentLoader,
        embedder: EmbeddingService,
        state_file: Path = DEFAULT_STATE_FILE,
    ) -> None:
        self._loader = loader
        self._embedder = embedder
        self._state_file = state_file
        self._chunks: list[Chunk] = []
        self._faiss_index: faiss.Index | None = None

    def build_or_load(self, force_rebuild: bool = False) -> None:
        if not force_rebuild and self._is_cache_valid():
            self._load_state()
        else:
            self._rebuild()

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[Chunk]:
        if self._faiss_index is None:
            raise RuntimeError("Index not initialised — call build_or_load() first.")
        vec = query_vector.reshape(1, -1).astype("float32")
        _, indices = self._faiss_index.search(vec, top_k)
        return [self._chunks[i] for i in indices[0] if i != -1]

    # ------------------------------------------------------------------

    def _is_cache_valid(self) -> bool:
        if not self._state_file.exists():
            return False
        try:
            with open(self._state_file, "rb") as f:
                state = pickle.load(f)
            return state.get("file_hashes", {}) == self._loader.compute_hashes()
        except Exception:
            return False

    def _load_state(self) -> None:
        with open(self._state_file, "rb") as f:
            state = pickle.load(f)
        self._chunks = [Chunk(**c) for c in state["chunks"]]
        self._faiss_index = faiss.deserialize_index(state["faiss_index"])
        print(f"[index] Loaded {len(self._chunks)} chunks from cache.")

    def _rebuild(self) -> None:
        print("[index] Rebuilding index…")
        records = self._loader.load_file_records()
        self._chunks = [c for r in records for c in r.chunks]

        print(f"[index] Embedding {len(self._chunks)} chunks…")
        vectors = self._embedder.embed_passages([c.text for c in self._chunks]).astype("float32")

        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        self._faiss_index = index

        state = {
            "file_hashes": {r.path.name: r.sha256 for r in records},
            "chunks": [asdict(c) for c in self._chunks],
            "faiss_index": faiss.serialize_index(index),
        }
        self._write_atomic(state)
        print(f"[index] Done — {len(self._chunks)} chunks indexed.")

    def _write_atomic(self, state: dict) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self._state_file.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, self._state_file)
        except Exception:
            os.unlink(tmp)
            raise

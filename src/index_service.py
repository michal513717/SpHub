"""
Manages the FAISS vector index and a single atomic state file.

State file layout (pickle):
  {
    "file_hashes":  dict[str, str],          # {filename: sha256}
    "chunks":       list[dict],              # serialised Chunk objects
    "faiss_index":  bytes,                   # faiss.serialize_index output
  }

The state file is written atomically (write to tmp → rename) so a crash
during a rebuild never leaves a half-written cache.

CQRS extensibility note:
  IndexService is a standalone class with a single public entry point
  `build_or_load(force_rebuild)`.  A future command-queue consumer (e.g., a
  file-watcher or polling worker) can instantiate this class and call
  `build_or_load(force_rebuild=True)` without touching the CLI or RAG layer.
"""

from __future__ import annotations

import os
import pickle
import tempfile
from dataclasses import asdict
from pathlib import Path

import faiss
import numpy as np

from src.document_loader import Chunk, DocumentLoader
from src.embedding_service import EmbeddingService

DEFAULT_STATE_FILE = Path(__file__).parent.parent / "data" / "index.pkl"


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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_or_load(self, force_rebuild: bool = False) -> None:
        """Load from cache if up-to-date, otherwise rebuild and persist."""
        if not force_rebuild and self._is_cache_valid():
            self._load_state()
            return
        self._rebuild()

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[Chunk]:
        if self._faiss_index is None:
            raise RuntimeError("Index not initialised — call build_or_load() first.")
        vec = query_vector.reshape(1, -1).astype("float32")
        distances, indices = self._faiss_index.search(vec, top_k)
        return [self._chunks[i] for i in indices[0] if i != -1]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_cache_valid(self) -> bool:
        if not self._state_file.exists():
            return False
        try:
            with open(self._state_file, "rb") as f:
                state = pickle.load(f)
            cached_hashes: dict[str, str] = state.get("file_hashes", {})
            current_hashes = self._loader.compute_hashes()
            return cached_hashes == current_hashes
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
        self._chunks = [chunk for r in records for chunk in r.chunks]

        texts = [c.text for c in self._chunks]
        print(f"[index] Embedding {len(texts)} chunks…")
        vectors = self._embedder.embed_passages(texts).astype("float32")

        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)  # inner-product on normalised vectors = cosine similarity
        index.add(vectors)
        self._faiss_index = index

        hashes = {r.path.name: r.sha256 for r in records}
        state = {
            "file_hashes": hashes,
            "chunks": [asdict(c) for c in self._chunks],
            "faiss_index": faiss.serialize_index(index),
        }
        self._write_state_atomic(state)
        print(f"[index] Done — {len(self._chunks)} chunks indexed.")

    def _write_state_atomic(self, state: dict) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=self._state_file.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp_path, self._state_file)
        except Exception:
            os.unlink(tmp_path)
            raise

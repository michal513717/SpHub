"""
Wraps intfloat/multilingual-e5-small via sentence-transformers.

E5 models require specific prefixes:
  - "passage: <text>"  when embedding document chunks for indexing
  - "query: <text>"    when embedding a user question for retrieval
"""

from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"


class EmbeddingService:
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self._model = SentenceTransformer(model_name)

    def embed_passages(self, texts: list[str]) -> np.ndarray:
        prefixed = [f"passage: {t}" for t in texts]
        return self._model.encode(prefixed, normalize_embeddings=True, show_progress_bar=False)

    def embed_query(self, text: str) -> np.ndarray:
        return self._model.encode(
            [f"query: {text}"],
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]

    @property
    def dimension(self) -> int:
        return self._model.get_sentence_embedding_dimension()

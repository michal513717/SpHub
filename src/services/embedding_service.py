from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from src.utils import EMBEDDING_MODEL


class EmbeddingService:
    """
    Wraps intfloat/multilingual-e5-small.
    E5 models require explicit prefixes for correct similarity scores:
      - "passage: <text>"  when indexing document chunks
      - "query: <text>"    when embedding a user question
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL) -> None:
        self._model = SentenceTransformer(model_name)

    def embed_passages(self, texts: list[str]) -> np.ndarray:
        return self._model.encode(
            [f"passage: {t}" for t in texts],
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def embed_query(self, text: str) -> np.ndarray:
        return self._model.encode(
            [f"query: {text}"],
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]

    @property
    def dimension(self) -> int:
        return self._model.get_sentence_embedding_dimension()

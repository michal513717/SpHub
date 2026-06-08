from __future__ import annotations

from src.services.embedding_service import EmbeddingService
from src.services.index_service import IndexService
from src.services.llm.base import AbstractLLMService
from src.types import AnswerQuery, AnswerResult, Chunk
from src.utils.constants import SYSTEM_PROMPT


class AnswerQueryHandler:
    """
    Read-side handler: retrieves relevant chunks and generates an answer.

    AbstractLLMService is injected, so swapping models (e.g. from haiku to opus,
    or to a local model) requires no changes here.
    """

    def __init__(
        self,
        index_service: IndexService,
        embedder: EmbeddingService,
        llm: AbstractLLMService,
    ) -> None:
        self._index = index_service
        self._embedder = embedder
        self._llm = llm

    def handle(self, query: AnswerQuery) -> AnswerResult:
        query_vec = self._embedder.embed_query(query.question)
        chunks: list[Chunk] = self._index.search(query_vec, top_k=query.top_k)

        context = "\n\n---\n\n".join(
            f"[{c.source_file}]\n{c.text}" for c in chunks
        )
        user_message = f"Fragmenty dokumentacji:\n\n{context}\n\nPytanie: {query.question}"

        answer = self._llm.complete(SYSTEM_PROMPT, user_message)
        return AnswerResult(answer=answer, source_chunks=chunks)

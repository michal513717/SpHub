"""
Orchestrates retrieval + answer generation.

Retrieval: FAISS cosine search via IndexService.
Generation: claude-haiku-4-5 via Anthropic SDK (streaming, adaptive thinking off
            — factographic Q&A doesn't need extended reasoning).
"""

from __future__ import annotations

import anthropic

from src.embedding_service import EmbeddingService
from src.index_service import IndexService

MODEL = "claude-haiku-4-5-20251001"
TOP_K = 5

SYSTEM_PROMPT = """\
Jesteś pomocnym asystentem obsługi klienta firmy SpaceHub — sieci biur coworkingowych w Krakowie.
Odpowiadaj wyłącznie na podstawie dostarczonych fragmentów dokumentacji.
Jeśli informacja nie jest zawarta w dokumentacji, powiedz to wprost — nie wymyślaj faktów.
Odpowiadaj po polsku, zwięźle i rzeczowo."""


class RAGService:
    def __init__(
        self,
        index: IndexService,
        embedder: EmbeddingService,
        anthropic_client: anthropic.Anthropic | None = None,
        top_k: int = TOP_K,
    ) -> None:
        self._index = index
        self._embedder = embedder
        self._client = anthropic_client or anthropic.Anthropic()
        self._top_k = top_k

    def answer(self, question: str) -> str:
        query_vec = self._embedder.embed_query(question)
        chunks = self._index.search(query_vec, top_k=self._top_k)

        context = "\n\n---\n\n".join(
            f"[{c.source_file}]\n{c.text}" for c in chunks
        )

        user_message = (
            f"Fragmenty dokumentacji:\n\n{context}\n\n"
            f"Pytanie: {question}"
        )

        full_response: list[str] = []
        with self._client.messages.stream(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response.append(text)

        print()  # newline after streamed output
        return "".join(full_response)

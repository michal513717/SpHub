"""
SpaceHub Q&A CLI

Usage:
    python main.py "Ile kosztuje hot desk basic?"
    python main.py --rebuild "Jakie są godziny otwarcia?"
    python main.py          # interactive mode (REPL)

Environment:
    ANTHROPIC_API_KEY   required for generation
"""

from __future__ import annotations

import argparse
import sys

from src.document_loader import DocumentLoader
from src.embedding_service import EmbeddingService
from src.index_service import IndexService
from src.rag_service import RAGService


def build_rag(force_rebuild: bool = False) -> RAGService:
    loader = DocumentLoader()
    embedder = EmbeddingService()
    index = IndexService(loader, embedder)
    index.build_or_load(force_rebuild=force_rebuild)
    return RAGService(index, embedder)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sphub-qa",
        description="SpaceHub knowledge-base Q&A powered by RAG + Claude",
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to answer (omit for interactive/REPL mode)",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force a full re-index even if the cache is current",
    )
    args = parser.parse_args()

    rag = build_rag(force_rebuild=args.rebuild)

    if args.question:
        rag.answer(args.question)
        return

    # Interactive REPL
    print("SpaceHub Q&A — wpisz pytanie lub 'exit' / Ctrl-C aby wyjść.\n")
    try:
        while True:
            try:
                question = input("Pytanie: ").strip()
            except EOFError:
                break
            if not question:
                continue
            if question.lower() in {"exit", "quit", "q"}:
                break
            rag.answer(question)
            print()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

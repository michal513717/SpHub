"""
SpaceHub Q&A CLI

Usage:
    python main.py "Ile kosztuje hot desk basic?"
    python main.py --rebuild "Jakie są godziny otwarcia?"
    python main.py                                          # interactive REPL

Environment:
    ANTHROPIC_API_KEY   required
"""

from __future__ import annotations

import argparse
import os
import sys

from src.commands.build_index import BuildIndexHandler
from src.queries.answer_question import AnswerQueryHandler
from src.services.document_loader_service import DocumentLoader
from src.services.embedding_service import EmbeddingService
from src.services.index_service import IndexService
from src.services.llm.claude import ClaudeLLMService
from src.types import AnswerQuery, BuildIndexCommand


def _build_handlers(force_rebuild: bool) -> AnswerQueryHandler:
    loader = DocumentLoader()
    embedder = EmbeddingService()
    index = IndexService(loader, embedder)

    BuildIndexHandler(index).handle(BuildIndexCommand(force_rebuild=force_rebuild))

    llm = ClaudeLLMService()          # swap model here: ClaudeLLMService(model="claude-opus-4-8")
    return AnswerQueryHandler(index, embedder, llm)


def _check_env() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Błąd: brak zmiennej środowiskowej ANTHROPIC_API_KEY.", file=sys.stderr)
        print("Ustaw klucz i spróbuj ponownie:", file=sys.stderr)
        print("  $env:ANTHROPIC_API_KEY = 'sk-ant-...'   # PowerShell", file=sys.stderr)
        print("  export ANTHROPIC_API_KEY='sk-ant-...'   # bash", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    _check_env()
    parser = argparse.ArgumentParser(
        prog="sphub-qa",
        description="SpaceHub knowledge-base Q&A powered by RAG + Claude",
    )
    parser.add_argument("question", nargs="?", help="Question (omit for interactive mode)")
    parser.add_argument("--rebuild", action="store_true", help="Force full re-index")
    args = parser.parse_args()

    handler = _build_handlers(force_rebuild=args.rebuild)

    if args.question:
        handler.handle(AnswerQuery(question=args.question))
        return

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
            handler.handle(AnswerQuery(question=question))
            print()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

from __future__ import annotations

from src.services.index_service import IndexService
from src.types import BuildIndexCommand


class BuildIndexHandler:
    """
    Write-side handler: builds or refreshes the vector index.

    This is the natural integration point for a future CQRS command queue
    (e.g., a polling worker that enqueues BuildIndexCommand when new files
    appear in knowledge/).  The handler itself is stateless — IndexService
    carries all mutable state.
    """

    def __init__(self, index_service: IndexService) -> None:
        self._index = index_service

    def handle(self, command: BuildIndexCommand) -> None:
        self._index.build_or_load(force_rebuild=command.force_rebuild)

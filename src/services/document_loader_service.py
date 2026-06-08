from __future__ import annotations

from pathlib import Path

from src.types import Chunk, FileRecord
from src.utils import KNOWLEDGE_DIR
from src.utils.utils import sha256_file, split_markdown


class DocumentLoader:
    """Scans the knowledge directory for .md files and produces chunks."""

    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
        self.knowledge_dir = knowledge_dir

    def load_file_records(self) -> list[FileRecord]:
        return [
            FileRecord(
                path=path,
                sha256=sha256_file(path),
                chunks=split_markdown(path.read_text(encoding="utf-8"), path.name),
            )
            for path in sorted(self.knowledge_dir.glob("*.md"))
        ]

    def compute_hashes(self) -> dict[str, str]:
        """Returns {filename: sha256} — used by IndexService for cache checks."""
        return {p.name: sha256_file(p) for p in sorted(self.knowledge_dir.glob("*.md"))}

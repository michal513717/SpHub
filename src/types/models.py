from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.utils.constants import TOP_K


@dataclass
class Chunk:
    text: str
    source_file: str
    chunk_index: int


@dataclass
class FileRecord:
    path: Path
    sha256: str
    chunks: list[Chunk] = field(default_factory=list)


@dataclass
class AnswerResult:
    answer: str
    source_chunks: list[Chunk]


@dataclass
class BuildIndexCommand:
    force_rebuild: bool = False


@dataclass
class AnswerQuery:
    question: str
    top_k: int = TOP_K

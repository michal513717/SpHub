"""
Reads .md files from the knowledge/ directory, computes file-level SHA-256 hashes,
and splits content into chunks that preserve header context (important for tables).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


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


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _split_markdown(text: str, source_file: str, max_chars: int = 800) -> list[Chunk]:
    """
    Splits markdown into chunks.
    Each chunk carries the nearest H1/H2/H3 header as a context prefix so that
    table rows and list items are never orphaned from their section title.
    """
    lines = text.splitlines(keepends=True)
    chunks: list[Chunk] = []
    current_headers: list[str] = []  # stack: [h1, h2, h3]
    current_block: list[str] = []
    in_table = False
    table_header: str | None = None

    def flush(block: list[str], idx: int) -> None:
        content = "".join(block).strip()
        if not content:
            return
        prefix = " > ".join(current_headers) + "\n\n" if current_headers else ""
        chunks.append(Chunk(
            text=prefix + content,
            source_file=source_file,
            chunk_index=idx,
        ))

    header_re = re.compile(r"^(#{1,3})\s+(.+)")
    separator_re = re.compile(r"^\s*\|[\s\-|]+\|\s*$")

    chunk_idx = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = header_re.match(line)
        if m:
            flush(current_block, chunk_idx)
            if current_block:
                chunk_idx += 1
            current_block = []
            in_table = False
            table_header = None

            level = len(m.group(1))
            title = m.group(2).strip()
            # Keep header stack up to current depth
            current_headers = current_headers[:level - 1]
            current_headers.append(title)
            i += 1
            continue

        # Detect table header row (contains | and the next line is a separator)
        if "|" in line and i + 1 < len(lines) and separator_re.match(lines[i + 1]):
            # Start of a new table — flush any pending non-table block first
            flush(current_block, chunk_idx)
            if current_block:
                chunk_idx += 1
            current_block = []
            in_table = True
            table_header = line
            current_block.append(line)
            i += 1
            continue

        if in_table and separator_re.match(line):
            current_block.append(line)
            i += 1
            continue

        if in_table and "|" in line:
            # Check if this row would make the chunk too long
            tentative = "".join(current_block) + line
            prefix_len = len(" > ".join(current_headers) + "\n\n") if current_headers else 0
            if prefix_len + len(tentative) > max_chars and len(current_block) > 2:
                # Flush current table chunk and start a new one with the header repeated
                flush(current_block, chunk_idx)
                chunk_idx += 1
                current_block = [table_header, lines[i - (len(current_block) - 1)]]  # re-add separator
                # safer: just restart with header + separator
                current_block = [table_header, ""]
                # find separator line right after original header
                for j, bl in enumerate(chunks[-1].text.splitlines()):
                    if separator_re.match(bl):
                        current_block = [table_header + "\n", bl + "\n"]
                        break
            current_block.append(line)
            i += 1
            continue

        # Non-table line
        if in_table:
            in_table = False
            table_header = None

        current_block.append(line)
        tentative = "".join(current_block)
        prefix_len = len(" > ".join(current_headers) + "\n\n") if current_headers else 0
        if prefix_len + len(tentative) >= max_chars:
            flush(current_block, chunk_idx)
            chunk_idx += 1
            current_block = []

        i += 1

    flush(current_block, chunk_idx)
    return chunks


class DocumentLoader:
    """Scans knowledge/ for .md files, hashes them, and produces chunks."""

    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR) -> None:
        self.knowledge_dir = knowledge_dir

    def load_file_records(self) -> list[FileRecord]:
        records: list[FileRecord] = []
        for path in sorted(self.knowledge_dir.glob("*.md")):
            sha = _sha256(path)
            chunks = _split_markdown(path.read_text(encoding="utf-8"), path.name)
            records.append(FileRecord(path=path, sha256=sha, chunks=chunks))
        return records

    def compute_hashes(self) -> dict[str, str]:
        """Returns {filename: sha256} for all .md files — used for cache checks."""
        return {
            p.name: _sha256(p)
            for p in sorted(self.knowledge_dir.glob("*.md"))
        }

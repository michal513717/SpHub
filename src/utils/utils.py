from __future__ import annotations

import hashlib
import re
from pathlib import Path

from src.types.models import Chunk


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def split_markdown(text: str, source_file: str, max_chars: int = 800) -> list[Chunk]:
    """
    Splits markdown into chunks, preserving the nearest H1/H2/H3 header as a
    context prefix so that table rows and list items are never orphaned from
    their section title.
    """
    lines = text.splitlines(keepends=True)
    chunks: list[Chunk] = []
    current_headers: list[str] = []
    current_block: list[str] = []
    in_table = False
    table_header: str | None = None

    header_re = re.compile(r"^(#{1,3})\s+(.+)")
    separator_re = re.compile(r"^\s*\|[\s\-|]+\|\s*$")

    chunk_idx = 0

    def flush(block: list[str]) -> None:
        nonlocal chunk_idx
        content = "".join(block).strip()
        if not content:
            return
        prefix = " > ".join(current_headers) + "\n\n" if current_headers else ""
        chunks.append(Chunk(text=prefix + content, source_file=source_file, chunk_index=chunk_idx))
        chunk_idx += 1

    def _prefix_len() -> int:
        return len(" > ".join(current_headers) + "\n\n") if current_headers else 0

    i = 0
    while i < len(lines):
        line = lines[i]

        m = header_re.match(line)
        if m:
            flush(current_block)
            current_block = []
            in_table = False
            table_header = None
            level = len(m.group(1))
            current_headers = current_headers[: level - 1]
            current_headers.append(m.group(2).strip())
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and separator_re.match(lines[i + 1]):
            flush(current_block)
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
            if _prefix_len() + len("".join(current_block) + line) > max_chars and len(current_block) > 2:
                flush(current_block)
                sep = next((l for l in current_block if separator_re.match(l)), "")
                current_block = [table_header, sep] if sep else [table_header]  # type: ignore[list-item]
            current_block.append(line)
            i += 1
            continue

        if in_table:
            in_table = False
            table_header = None

        current_block.append(line)
        if _prefix_len() + len("".join(current_block)) >= max_chars:
            flush(current_block)
            current_block = []

        i += 1

    flush(current_block)
    return chunks

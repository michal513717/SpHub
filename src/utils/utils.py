from __future__ import annotations

import hashlib
import re
from pathlib import Path

from src.types.models import Chunk


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def split_markdown(text: str, source_file: str) -> list[Chunk]:
    """
    Splits markdown into chunks at H1/H2/H3 header boundaries.

    Each chunk = one section (everything between two successive headers).
    The full header path (e.g. "Plans > Hot Desk") is prepended as context
    so table rows and list items are never orphaned from their section title.
    """
    header_re = re.compile(r"^(#{1,3})\s+(.+)")

    chunks: list[Chunk] = []
    current_headers: list[str] = []
    current_block: list[str] = []
    chunk_idx = 0

    def flush(block: list[str]) -> None:
        nonlocal chunk_idx
        content = "".join(block).strip()
        if not content:
            return
        prefix = " > ".join(current_headers) + "\n\n" if current_headers else ""
        chunks.append(Chunk(text=prefix + content, source_file=source_file, chunk_index=chunk_idx))
        chunk_idx += 1

    for line in text.splitlines(keepends=True):
        m = header_re.match(line)
        if m:
            flush(current_block)
            current_block = []
            level = len(m.group(1))
            current_headers = current_headers[: level - 1]
            current_headers.append(m.group(2).strip())
        else:
            current_block.append(line)

    flush(current_block)
    return chunks

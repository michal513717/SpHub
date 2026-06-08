# SpaceHub Q&A

CLI tool that answers questions about the SpaceHub coworking network using
Retrieval-Augmented Generation (RAG).

**Stack:**
- Embeddings: `intfloat/multilingual-e5-small` (local, ~120 MB, Polish-aware)
- Vector index: FAISS (local, no external DB)
- Generation: `claude-haiku-4-5` via Anthropic API (streaming)
- Cache: SHA-256 file-level hash — re-indexes only when source files change

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Set your Anthropic API key:

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-...."

# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

```bash
# Single question
python main.py "Ile kosztuje hot desk basic?"

# Force full re-index (e.g. after editing knowledge files)
python main.py --rebuild "Jakie są okresy wypowiedzenia?"

# Interactive REPL (ask multiple questions)
python main.py
```

## Project layout

```
SpHub/
├── knowledge/          # Source documents (read-only)
│   ├── 01-company-overview.md
│   └── …
├── src/
│   ├── document_loader.py   # File hashing + markdown chunking
│   ├── embedding_service.py # multilingual-e5-small wrapper
│   ├── index_service.py     # FAISS index + atomic state file
│   └── rag_service.py       # Retrieval + Claude generation
├── data/               # Generated cache — gitignored, auto-rebuilt
│   └── index.pkl
├── main.py             # CLI entry point
└── requirements.txt
```

## How caching works

On first run (or after `--rebuild`) the tool:

1. Reads all `.md` files from `knowledge/`
2. Computes a SHA-256 hash per file
3. Splits each file into chunks (headers preserved as context for table rows)
4. Embeds all chunks with `multilingual-e5-small`
5. Builds a FAISS inner-product index
6. Writes everything atomically to `data/index.pkl`

On subsequent runs it compares stored hashes against current file hashes.
If they match, the index is loaded from cache (~1 s).  If any file changed or
a new file was added, the entire index is rebuilt.

## Extending to an API / CQRS

`IndexService` is intentionally a standalone class — it can be triggered from
any context (CLI, HTTP handler, queue consumer) by calling:

```python
index = IndexService(loader, embedder)
index.build_or_load(force_rebuild=True)
```

A future file-watching worker (e.g., polling `knowledge/` every N seconds or
every M new files) would simply instantiate `IndexService` and call this method
without any changes to the core pipeline.

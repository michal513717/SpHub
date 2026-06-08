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
├── knowledge/       # Source documents (read-only, 15 .md files)
├── src/
│   ├── utils/
│   ├── types/
│   ├── services/
│   │   └── llm/
│   ├── commands/
│   └── queries/
├── data/            # Generated cache (.gitignored)
├── main.py
├── requirements.txt
└── README.md
```

## How it works

### Caching strategy

On first run (or after `--rebuild`):

1. Read all `.md` files from `knowledge/` → compute SHA-256 hash per file
2. Split each file into chunks at H1/H2/H3 header boundaries (preserves full context, no mid-table splits)
3. Embed all chunks with `multilingual-e5-small` (with `"passage: "` prefix)
4. Build FAISS `IndexFlatIP` (inner-product, normalized = cosine similarity)
5. Write atomically to `data/index.pkl`:
   - `file_hashes`: {filename: sha256}
   - `chunks`: serialized Chunk objects  
   - `faiss_index`: binary FAISS index

On subsequent runs:
- Compare stored hashes vs. current file hashes
- If match → load from cache (~1 s)
- If mismatch (any file changed/added) → rebuild entire index

### Query flow

1. User asks a question
2. Embed query with `"query: "` prefix → 384-dim vector
3. FAISS search → top 5 most similar chunks
4. Format chunks as context → send to Claude
5. Stream response from Claude (tokenized real-time)
6. Return answer + source chunks

## Architecture notes

### CQRS separation

The codebase is structured as CQRS (Command Query Responsibility Segregation):

- **Write side**: `BuildIndexHandler` — rebuilds the index (triggered by `BuildIndexCommand`)
- **Read side**: `AnswerQueryHandler` — retrieves chunks and generates answers (uses `AnswerQuery`)
- **State**: `IndexService` — mutable repository (FAISS index + file hashes)
- **LLM injection**: `AbstractLLMService` — swap `ClaudeLLMService` for any other provider without touching retrieval logic

### Extending to an API / async queue

Current wiring in `main.py`:

```python
BuildIndexHandler(index).handle(BuildIndexCommand(force_rebuild=args.rebuild))
llm = ClaudeLLMService()
handler = AnswerQueryHandler(index, embedder, llm)
handler.handle(AnswerQuery(question="..."))
```

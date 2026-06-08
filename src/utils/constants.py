from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent  # src/utils/constants.py → project root

KNOWLEDGE_DIR: Path = _ROOT / "knowledge"
DEFAULT_STATE_FILE: Path = _ROOT / "data" / "index.pkl"

EMBEDDING_MODEL: str = "intfloat/multilingual-e5-small"
CLAUDE_MODEL: str = "claude-haiku-4-5-20251001"

TOP_K: int = 5
MAX_CHUNK_CHARS: int = 800

SYSTEM_PROMPT: str = """\
Jesteś pomocnym asystentem obsługi klienta firmy SpaceHub — sieci biur coworkingowych w Krakowie.
Odpowiadaj wyłącznie na podstawie dostarczonych fragmentów dokumentacji.
Jeśli informacja nie jest zawarta w dokumentacji, powiedz to wprost — nie wymyślaj faktów.
Odpowiadaj po polsku, zwięźle i rzeczowo."""

from __future__ import annotations

import anthropic

from src.services.llm.base import AbstractLLMService
from src.utils import CLAUDE_MODEL


class ClaudeLLMService(AbstractLLMService):
    """
    Anthropic Claude backend.

    Args:
        model:            Any claude-* model string (defaults to CLAUDE_MODEL constant).
        client:           Provide a pre-configured client for testing / custom auth.
        stream_to_stdout: When True, tokens are printed as they arrive (CLI mode).
                          Set to False for API/worker contexts where the caller
                          wants only the returned string.
    """

    def __init__(
        self,
        model: str = CLAUDE_MODEL,
        client: anthropic.Anthropic | None = None,
        stream_to_stdout: bool = True,
    ) -> None:
        super().__init__()
        self._model = model
        self._client = client or anthropic.Anthropic()
        self._stream_to_stdout = stream_to_stdout

    def complete(self, system: str, user_message: str) -> str:
        parts: list[str] = []
        with self._client.messages.stream(
            model=self._model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                if self._stream_to_stdout:
                    print(text, end="", flush=True)
                parts.append(text)

        if self._stream_to_stdout:
            print()
        return "".join(parts)

from abc import ABC, abstractmethod


class AbstractLLMService(ABC):
    """
    Abstraction over any text-completion backend.
    Inject a concrete implementation into query handlers — this lets you swap
    models (or providers) without touching retrieval logic.
    """

    @abstractmethod
    def complete(self, system: str, user_message: str) -> str:
        """Returns the full response text."""
        ...

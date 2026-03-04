"""Agent基类"""

from abc import ABC, abstractmethod
from typing import Optional, Any
from .message import Message
from .llm import HelloAgentLLM
from .config import Config


class Agent(ABC):
    def __init__(
        self,
        name: str,
        llm: HelloAgentLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config or Config()
        self._history: list[Message] = []

    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        pass

    def add_message(self, message: Message):
        self._history.append(message)

    def clear_history(self):
        self._history.clear()

    def get_history(self) -> list[Message]:
        return self._history

    def __str__(self):
        return f"Agent(name={self.name}, provider={self.llm.provider})"

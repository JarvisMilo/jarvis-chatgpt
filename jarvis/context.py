from __future__ import annotations

from dataclasses import dataclass, field
from .llm import ChatMessage


@dataclass
class ConversationContext:
    system_prompt: str
    max_messages: int = 12
    history: list[ChatMessage] = field(default_factory=list)
    tool_results: list[ChatMessage] = field(default_factory=list)

    def add_user(self, content: str) -> None:
        self.history.append(ChatMessage("user", content))
        self._trim()

    def add_assistant(self, content: str) -> None:
        self.history.append(ChatMessage("assistant", content))
        self._trim()

    def add_tool_result(self, content: str) -> None:
        self.tool_results.append(ChatMessage("system", content))

    def messages(self, memory_text: str = "", tool_catalog: str = "") -> list[ChatMessage]:
        result = [ChatMessage("system", self.system_prompt)]
        if memory_text:
            result.append(ChatMessage("system", memory_text))
        if tool_catalog:
            result.append(ChatMessage("system", tool_catalog))
        result.extend(self.tool_results[-5:])
        result.extend(self.history[-self.max_messages:])
        return result

    def _trim(self) -> None:
        if len(self.history) > self.max_messages:
            del self.history[:-self.max_messages]

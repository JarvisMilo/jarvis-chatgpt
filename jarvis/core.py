from __future__ import annotations
from .config import Settings
from .llm import ChatMessage, LLMProvider
from .memory import MemoryRepository
from .tools import ToolRegistry,Tool,safe_ping

SYSTEM_PROMPT="""You are JARVIS, a local-first personal assistant. Be precise, calm and action-oriented.
You are running locally. Never claim an action was executed unless a real tool result confirms it."""
class JarvisCore:
    def __init__(self,settings:Settings,provider:LLMProvider,memory:MemoryRepository,tools:ToolRegistry):
        self.settings=settings; self.provider=provider; self.memory=memory; self.tools=tools
        self.history:list[ChatMessage]=[]
    def register_defaults(self):
        if not any(t.name=="ping" for t in self.tools.list()):
            self.tools.register(Tool("ping","Safe health-check tool.",safe_ping))
    def stream_chat(self,user_text:str):
        self.history.append(ChatMessage("user",user_text))
        memories=self.memory.recent(5)
        memory_text="\n".join(f"- {m.kind}: {m.content}" for m in memories)
        messages=[ChatMessage("system",SYSTEM_PROMPT)]
        if memory_text: messages.append(ChatMessage("system","Relevant recent memory:\n"+memory_text))
        messages.extend(self.history[-12:])
        full=""
        for chunk in self.provider.chat(messages,stream=True):
            full+=chunk
            yield chunk
        self.history.append(ChatMessage("assistant",full))

from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Capability:
    name: str
    category: str
    level: int
    status: str
    local: bool = True
    description: str = ""

class CapabilityRegistry:
    def __init__(self): self._items: dict[str, Capability] = {}
    def register(self, capability: Capability): self._items[capability.name] = capability
    def all(self): return list(self._items.values())
    def by_category(self, category: str): return [x for x in self._items.values() if x.category == category]
    def snapshot(self): return [x.__dict__.copy() for x in self._items.values()]

def default_capabilities():
    r = CapabilityRegistry()
    items = [
        ("ollama","llm",1,"IMPLEMENTED",True,"Local LLM provider"),("memory","core",1,"IMPLEMENTED",True,"Persistent local memory"),
        ("tool_registry","core",1,"IMPLEMENTED",True,"Typed tool boundary"),("agents","agents",2,"IMPLEMENTED",True,"20 specialized agent contracts"),
        ("windows","desktop",3,"IN_PROGRESS",True,"Windows adapters"),("browser","web",3,"IN_PROGRESS",True,"Playwright adapter"),
        ("vision","vision",4,"IN_PROGRESS",True,"Screen/visual adapter"),("voice","voice",4,"IN_PROGRESS",True,"Local speech architecture"),
        ("research","intelligence",5,"IN_PROGRESS",True,"Search and provenance"),("documents","productivity",5,"IN_PROGRESS",True,"Document processing"),
        ("automation","automation",5,"IN_PROGRESS",True,"Tasks and reminders"),("communications","integrations",6,"PLANNED",False,"External messaging adapters"),
        ("remote","remote",6,"IN_PROGRESS",True,"Authenticated gateway boundary"),("ambient_ui","ui",6,"IN_PROGRESS",True,"Original PyQt6 ambient HUD"),
    ]
    for x in items: r.register(Capability(*x))
    return r

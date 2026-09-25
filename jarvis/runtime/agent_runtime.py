from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from jarvis.agents import BuiltinAgent, build_builtin_agents

@dataclass
class AgentExecution:
    execution_id: str
    agent: str
    status: str = "QUEUED"
    started_at: str | None = None
    finished_at: str | None = None
    result: dict[str, Any] | None = None
    error: str | None = None

class AgentRuntime:
    def __init__(self):
        self.agents: dict[str, BuiltinAgent] = build_builtin_agents()
        self.history: list[AgentExecution] = []
    def list_agents(self) -> list[dict[str, Any]]:
        return [{"name": a.name, "mission": a.mission, "capabilities": list(a.capabilities)} for a in self.agents.values()]
    def run(self, agent: str, payload: dict[str, Any], execution_id: str) -> AgentExecution:
        if agent not in self.agents: raise KeyError(f"Unknown agent: {agent}")
        item = AgentExecution(execution_id, agent, "RUNNING", datetime.now(timezone.utc).isoformat())
        try:
            item.result = self.agents[agent].run(payload); item.status = "SUCCESS"
        except Exception as exc:
            item.status = "FAILED"; item.error = str(exc)
        item.finished_at = datetime.now(timezone.utc).isoformat(); self.history.append(item); return item

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class AgentStatus(str, Enum): IDLE="IDLE"; RUNNING="RUNNING"; BLOCKED="BLOCKED"; FAILED="FAILED"
@dataclass(frozen=True)
class AgentSpec:
    name: str; mission: str; tools: tuple[str,...]=(); context: tuple[str,...]=(); limits: tuple[str,...]=(); permission: str="LOW"
@dataclass
class AgentResult:
    agent: str; success: bool; output: Any=None; error: str|None=None
class AgentRegistry:
    def __init__(self) -> None: self._agents: dict[str,AgentSpec]={}
    def register(self,spec:AgentSpec)->None:
        if spec.name in self._agents: raise ValueError(f"Duplicate agent: {spec.name}")
        self._agents[spec.name]=spec
    def get(self,name:str)->AgentSpec: return self._agents[name]
    def list(self)->list[AgentSpec]: return list(self._agents.values())

def default_agents()->AgentRegistry:
    r=AgentRegistry()
    data=[("Orchestrator","Coordinates tasks and agents"),("Planner","Breaks goals into verified steps"),("Computer Control","Controls approved Windows UI"),("File System","Performs policy-bound file operations"),("Browser","Automates approved browser tasks"),("Research","Collects and cites information"),("Coding","Builds and tests software"),("Git DevOps","Manages repositories and CI"),("Vision","Interprets screenshots and UI"),("Voice","Handles local speech input/output"),("Memory","Maintains persistent contextual memory"),("System Monitor","Observes system health"),("Automation","Schedules and runs approved tasks"),("Security Policy","Evaluates permissions and risks"),("QA Verification","Verifies outcomes and recovery")]
    for name,mission in data: r.register(AgentSpec(name,mission))
    return r

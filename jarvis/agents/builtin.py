from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class BuiltinAgent:
    name: str
    mission: str
    capabilities: tuple[str, ...]
    handler: Callable[[dict[str, Any]], dict[str, Any]]
    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.handler(payload)

def _echo(role: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"success": True, "agent": role, "output": payload, "mode": "contracted-local-execution"}

def build_builtin_agents() -> dict[str, BuiltinAgent]:
    specs = [
        ("Orchestrator","Coordinates execution and lifecycle",("tasks","events","state")),
        ("Planner","Converts goals into ordered, verifiable steps",("planning","dependencies","verification")),
        ("Computer Control","Controls approved Windows interactions",("windows","input","apps")),
        ("File System","Performs policy-bound filesystem work",("files","documents","undo")),
        ("Browser","Operates an isolated browser session",("navigation","forms","extraction")),
        ("Research","Collects and preserves source provenance",("search","sources","research")),
        ("Coding","Inspects, edits and tests local projects",("code","tests","debug")),
        ("Git DevOps","Performs safe repository workflows",("git","diff","ci")),
        ("Vision","Interprets screenshots and visual observations",("screen","ocr","vision")),
        ("Voice","Coordinates local speech adapters",("stt","tts","wake")),
        ("Memory","Retrieves and updates persistent context",("memory","recall","forget")),
        ("System Monitor","Observes Windows resources and health",("cpu","ram","gpu","network")),
        ("Automation","Schedules bounded background work",("scheduler","reminders","notifications")),
        ("Security Policy","Evaluates risk, permission and confirmation",("policy","audit","trust")),
        ("QA Verification","Checks outcomes and triggers bounded recovery",("verify","diagnose","recover")),
        ("Media","Controls approved local/media workflows",("youtube","playback","volume")),
        ("Communications","Routes external messages through confirmation gates",("email","telegram","whatsapp")),
        ("Presentation","Builds document and presentation artifacts",("pptx","docx","xlsx")),
        ("Personalization","Maintains identity, UI and behavior preferences",("theme","voice","profile")),
        ("Remote Gateway","Provides authenticated remote status/control boundaries",("pairing","auth","revocation")),
    ]
    return {name: BuiltinAgent(name, mission, caps, lambda payload, n=name: _echo(n, payload)) for name, mission, caps in specs}

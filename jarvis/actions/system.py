from __future__ import annotations
import platform
from jarvis.tools import RiskLevel, Tool
from jarvis.windows.system import system_snapshot

def _snapshot() -> dict[str, object]:
    data = system_snapshot()
    data["platform"] = platform.platform()
    return data

TOOL = Tool(
    name="system_snapshot",
    description="Read a local, non-mutating system snapshot.",
    handler=_snapshot,
    parameters={"type": "object", "properties": {}, "required": []},
    risk=RiskLevel.SAFE,
    category="system",
)

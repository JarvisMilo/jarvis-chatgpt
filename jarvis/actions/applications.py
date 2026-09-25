from __future__ import annotations
from jarvis.tools import RiskLevel, Tool
from jarvis.windows.applications import discover_applications

def _discover() -> list[dict[str, object]]:
    return [{"name": a.name, "executable": a.executable, "source": a.source, "arguments": a.arguments}
            for a in discover_applications()]

TOOL = Tool(
    name="discover_applications",
    description="Discover local applications without launching them.",
    handler=_discover,
    parameters={"type": "object", "properties": {}, "required": []},
    risk=RiskLevel.SAFE,
    category="windows.discovery",
)

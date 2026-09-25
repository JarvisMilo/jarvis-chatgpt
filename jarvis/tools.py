from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable


class ToolError(RuntimeError):
    pass


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    REVERSIBLE = "REVERSIBLE"
    SENSITIVE = "SENSITIVE"
    DANGEROUS = "DANGEROUS"
    EXTERNAL_SIDE_EFFECT = "EXTERNAL_SIDE_EFFECT"


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]
    parameters: dict[str, Any]
    risk: RiskLevel = RiskLevel.SAFE
    reversible: bool = False
    requires_confirmation: bool = False
    category: str = "general"

    def definition(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "risk": self.risk.value,
            "reversible": self.reversible,
            "requires_confirmation": self.requires_confirmation,
            "category": self.category,
        }


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if not tool.name or not tool.name.replace("_", "").isalnum():
            raise ToolError("Invalid tool name")
        if tool.name in self._tools:
            raise ToolError(f"Duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolError(f"Unknown tool: {name}") from exc

    def list(self) -> list[Tool]:
        return list(self._tools.values())

    def definitions(self) -> list[dict[str, Any]]:
        return [tool.definition() for tool in self.list()]

    def execute(self, name: str, *, confirmed: bool = False, **kwargs: Any) -> dict[str, Any]:
        tool = self.get(name)
        try:
            _validate_parameters(tool.parameters, kwargs)
        except ToolError as exc:
            return _result(False, error=str(exc))

        gated = (
            tool.requires_confirmation
            or tool.risk in {RiskLevel.SENSITIVE, RiskLevel.DANGEROUS, RiskLevel.EXTERNAL_SIDE_EFFECT}
        )
        if gated and not confirmed:
            return _result(False, error="CONFIRMATION_REQUIRED")

        try:
            data = tool.handler(**kwargs)
            return _result(True, data=data)
        except Exception as exc:
            return _result(False, error=f"{type(exc).__name__}: {exc}")


def _validate_parameters(schema: dict[str, Any], values: dict[str, Any]) -> None:
    if not isinstance(schema, dict):
        raise ToolError("Invalid tool schema")
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    if not isinstance(properties, dict) or not isinstance(required, list):
        raise ToolError("Invalid tool schema")
    unknown = set(values) - set(properties)
    if unknown:
        raise ToolError(f"Unknown parameters: {', '.join(sorted(unknown))}")
    missing = [name for name in required if name not in values]
    if missing:
        raise ToolError(f"Missing parameters: {', '.join(missing)}")
    for name, value in values.items():
        expected = properties[name].get("type")
        if expected == "string" and not isinstance(value, str):
            raise ToolError(f"Parameter '{name}' must be a string")
        if expected == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            raise ToolError(f"Parameter '{name}' must be an integer")
        if expected == "boolean" and not isinstance(value, bool):
            raise ToolError(f"Parameter '{name}' must be a boolean")


def _result(success: bool, *, data: Any = None, error: str | None = None) -> dict[str, Any]:
    return {"success": success, "data": data, "error": error, "warnings": [], "artifacts": []}


def safe_ping() -> str:
    return "pong"


def workspace_list(workspace: Path, relative_path: str = ".") -> list[str]:
    root = workspace.resolve()
    candidate = (root / relative_path).resolve()
    if candidate != root and root not in candidate.parents:
        raise ToolError("Path is outside the JARVIS workspace")
    if not candidate.exists():
        raise ToolError("Workspace path does not exist")
    if not candidate.is_dir():
        raise ToolError("Workspace path is not a directory")
    return sorted(item.name for item in candidate.iterdir())


def default_tools(workspace: Path) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        Tool(
            "ping",
            "Return a local health-check response.",
            safe_ping,
            {"type": "object", "properties": {}, "required": []},
            category="diagnostics",
        )
    )
    registry.register(
        Tool(
            "workspace_list",
            "List entries inside the configured JARVIS workspace only.",
            lambda relative_path=".": workspace_list(workspace, relative_path),
            {
                "type": "object",
                "properties": {"relative_path": {"type": "string"}},
                "required": [],
            },
            category="filesystem",
        )
    )
    return registry

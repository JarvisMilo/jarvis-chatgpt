from __future__ import annotations
import importlib
import pkgutil
from dataclasses import dataclass
from typing import Any
from jarvis.tools import Tool, ToolError

@dataclass(frozen=True)
class PluginSpec:
    name: str
    version: str
    description: str
    permissions: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()

class PluginLoader:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginSpec] = {}

    def discover(self, package: str = "jarvis.plugins") -> list[PluginSpec]:
        pkg = importlib.import_module(package)
        for item in pkgutil.iter_modules(pkg.__path__, package + "."):
            if item.name.rsplit(".", 1)[-1].startswith("_") or item.name.endswith(".loader"):
                continue
            self.load(item.name)
        return list(self._plugins.values())

    def load(self, module_name: str) -> PluginSpec:
        module = importlib.import_module(module_name)
        raw: Any = getattr(module, "PLUGIN", None)
        if not isinstance(raw, dict):
            raise ToolError(f"{module_name}.PLUGIN must be a mapping")
        name = str(raw.get("name", "")).strip()
        if not name:
            raise ToolError(f"{module_name} has no plugin name")
        spec = PluginSpec(
            name=name,
            version=str(raw.get("version", "0.0.0")),
            description=str(raw.get("description", "")),
            permissions=tuple(str(x) for x in raw.get("permissions", ())),
            tools=tuple(getattr(module, "TOOL").name for _ in [0])
            if getattr(module, "TOOL", None) is not None else (),
        )
        if spec.name in self._plugins:
            raise ToolError(f"Duplicate plugin: {spec.name}")
        tool = getattr(module, "TOOL", None)
        if tool is not None and not isinstance(tool, Tool):
            raise ToolError(f"{module_name}.TOOL must be a Tool instance")
        self._plugins[spec.name] = spec
        return spec

    def list(self) -> list[PluginSpec]:
        return list(self._plugins.values())

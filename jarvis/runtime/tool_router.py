from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Any

from jarvis.runtime.journal import ActionJournal, ActionRecord
from jarvis.runtime.permissions import PermissionBroker, PermissionLevel
from jarvis.tools import RiskLevel, Tool, ToolError, ToolRegistry

_RISK_TO_PERMISSION = {
    RiskLevel.SAFE: PermissionLevel.LOW,
    RiskLevel.REVERSIBLE: PermissionLevel.MEDIUM,
    RiskLevel.SENSITIVE: PermissionLevel.HIGH,
    RiskLevel.DANGEROUS: PermissionLevel.HIGH,
    RiskLevel.EXTERNAL_SIDE_EFFECT: PermissionLevel.HIGH,
}

class ToolRouter:
    """Single execution boundary for discovered tools."""
    def __init__(self, registry=None, broker=None, journal=None) -> None:
        self.registry = registry or ToolRegistry()
        self.broker = broker or PermissionBroker()
        self.journal = journal or ActionJournal()

    def discover_package(self, package: str) -> list[str]:
        loaded = []
        pkg = importlib.import_module(package)
        for item in pkgutil.iter_modules(pkg.__path__, package + "."):
            if item.name.rsplit(".", 1)[-1].startswith("_"):
                continue
            loaded.append(self._load_module(item.name))
        return loaded

    def discover_directory(self, directory: Path, package_prefix: str | None = None) -> list[str]:
        if not directory.exists():
            return []
        if not package_prefix:
            raise ToolError("package_prefix is required for safe directory discovery")
        return self.discover_package(package_prefix)

    def load_module(self, module_name: str) -> str:
        return self._load_module(module_name)

    def _load_module(self, module_name: str) -> str:
        module = importlib.import_module(module_name)
        tool = getattr(module, "TOOL", None)
        if tool is None:
            return module_name
        if not isinstance(tool, Tool):
            raise ToolError(f"{module_name}.TOOL must be a Tool instance")
        self.registry.register(tool)
        return tool.name

    def execute(self, name: str, *, confirmed=False, authenticated=False, **kwargs: Any) -> dict[str, Any]:
        tool = self.registry.get(name)
        level = _RISK_TO_PERMISSION[tool.risk]
        decision = self.broker.decide(level, confirmed=confirmed, authenticated=authenticated)
        if not decision.allowed:
            return {
                "success": False, "data": None,
                "error": "CONFIRMATION_REQUIRED" if decision.requires_confirmation else decision.reason,
                "warnings": [decision.reason] if decision.requires_confirmation else [],
                "artifacts": [],
            }
        result = self.registry.execute(name, confirmed=True, **kwargs)
        if result["success"]:
            self.journal.record(ActionRecord(
                action_id=self.journal.next_id(), tool=name, arguments=kwargs,
                result=result.get("data"), reversible=tool.reversible,
            ))
        return result

    def definitions(self) -> list[dict[str, Any]]:
        return self.registry.definitions()

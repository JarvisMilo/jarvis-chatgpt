import pytest

from jarvis.tools import RiskLevel, Tool, ToolError, ToolRegistry, default_tools, safe_ping


def test_register_and_execute():
    registry = ToolRegistry()
    registry.register(Tool("ping", "safe", safe_ping, {"type": "object", "properties": {}, "required": []}))
    result = registry.execute("ping")
    assert result == {"success": True, "data": "pong", "error": None, "warnings": [], "artifacts": []}


def test_duplicate_and_unknown_rejected():
    registry = ToolRegistry()
    registry.register(Tool("ping", "safe", safe_ping, {"type": "object", "properties": {}, "required": []}))
    with pytest.raises(ToolError):
        registry.register(Tool("ping", "safe", safe_ping, {"type": "object", "properties": {}, "required": []}))
    with pytest.raises(ToolError):
        registry.execute("missing")


def test_schema_and_confirmation():
    registry = ToolRegistry()
    registry.register(
        Tool(
            "danger",
            "danger",
            lambda value: value,
            {"type": "object", "properties": {"value": {"type": "string"}}, "required": ["value"]},
            risk=RiskLevel.DANGEROUS,
        )
    )
    assert registry.execute("danger", value="x")["error"] == "CONFIRMATION_REQUIRED"
    assert registry.execute("danger", confirmed=True, value="x")["data"] == "x"
    assert registry.execute("danger", value=3)["error"].startswith("CONFIRMATION_REQUIRED")


def test_workspace_tool_is_contained(tmp_path):
    registry = default_tools(tmp_path)
    assert registry.execute("workspace_list", relative_path=".")["success"]
    result = registry.execute("workspace_list", relative_path="..")
    assert result["success"] is False
    assert "outside" in result["error"]

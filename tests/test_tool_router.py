from jarvis.runtime.permissions import PermissionBroker, PermissionLevel
from jarvis.runtime.tool_router import ToolRouter
from jarvis.tools import RiskLevel, Tool, ToolError


def test_discover_builtin_actions():
    router = ToolRouter()
    names = router.discover_package("jarvis.actions")
    assert "system_snapshot" in names
    assert "discover_applications" in names
    assert "open_url" in names


def test_router_gates_external_side_effects():
    router = ToolRouter()
    router.load_module("jarvis.actions.web")
    result = router.execute("open_url", url="https://example.com")
    assert result["success"] is False
    assert result["error"] == "CONFIRMATION_REQUIRED"


def test_router_executes_safe_action_and_journals():
    router = ToolRouter()
    router.load_module("jarvis.actions.system")
    result = router.execute("system_snapshot")
    assert result["success"] is True
    assert router.journal.last() is not None
    assert router.journal.last().tool == "system_snapshot"


def test_critical_requires_authentication_before_confirmation():
    broker = PermissionBroker(max_level=PermissionLevel.CRITICAL)
    decision = broker.decide(PermissionLevel.CRITICAL, confirmed=True)
    assert not decision.allowed
    assert decision.requires_authentication

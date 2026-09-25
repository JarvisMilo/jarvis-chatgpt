import pytest
from jarvis.tools import ToolRegistry,Tool,ToolError,safe_ping

def test_register_and_execute():
    r=ToolRegistry(); r.register(Tool("ping","safe",safe_ping))
    assert r.execute("ping")["data"]=="pong"

def test_duplicate_rejected():
    r=ToolRegistry(); r.register(Tool("ping","safe",safe_ping))
    with pytest.raises(ToolError): r.register(Tool("ping","safe",safe_ping))

def test_dangerous_requires_confirmation():
    r=ToolRegistry(); r.register(Tool("danger","x",lambda:None,risk="DANGEROUS"))
    assert r.execute("danger")["error"]=="CONFIRMATION_REQUIRED"

from jarvis.windows.system import snapshot
from jarvis.windows.applications import discover_applications

def test_system_snapshot_has_core_fields():
    data=snapshot(); assert "os" in data and "python" in data

def test_application_discovery_is_list():
    assert isinstance(discover_applications(), list)

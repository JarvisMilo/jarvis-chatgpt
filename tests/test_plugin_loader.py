import sys
import types

from jarvis.plugins.loader import PluginLoader
from jarvis.tools import RiskLevel, Tool


def test_plugin_loader_validates_metadata():
    module = types.ModuleType("jarvis.plugins.test_plugin")
    module.PLUGIN = {
        "name": "test-plugin",
        "version": "1.0.0",
        "description": "test",
        "permissions": ["read"],
    }
    module.TOOL = Tool(
        "test_plugin_tool",
        "test",
        lambda: "ok",
        {"type": "object", "properties": {}, "required": []},
        risk=RiskLevel.SAFE,
    )
    sys.modules[module.__name__] = module
    try:
        spec = PluginLoader().load(module.__name__)
        assert spec.name == "test-plugin"
        assert spec.tools == ("test_plugin_tool",)
    finally:
        sys.modules.pop(module.__name__, None)

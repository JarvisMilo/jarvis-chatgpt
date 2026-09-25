from jarvis.core import JarvisCore
from jarvis.memory import MemoryRepository
from jarvis.tools import default_tools
from jarvis.config import load_settings
from jarvis.llm import ChatMessage


class FakeProvider:
    def __init__(self):
        self.messages = None

    def chat(self, messages, *, stream=True):
        self.messages = list(messages)
        yield "OK"
        yield "!"


def test_core_stream_and_context(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings = load_settings()
    memory = MemoryRepository(settings.db_path)
    memory.save("preference", "Spanish")
    provider = FakeProvider()
    core = JarvisCore(settings, provider, memory, default_tools(settings.workspace))
    assert "".join(core.stream_chat("hello")) == "OK!"
    assert provider.messages[0] == ChatMessage("system", provider.messages[0].content)
    assert any("Spanish" in m.content for m in provider.messages)
    assert core.context.history[-1].content == "OK!"

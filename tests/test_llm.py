import io
import json
import urllib.error

import pytest

from jarvis.llm import ChatMessage, LLMError, OllamaProvider


class FakeResponse:
    def __init__(self, chunks):
        self.chunks = chunks
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.closed = True

    def __iter__(self):
        return iter(self.chunks)

    def read(self):
        return b"".join(self.chunks)


def test_streaming_parses_jsonl(monkeypatch):
    response = FakeResponse([
        b'{"message":{"content":"Hel"}}\n',
        b'{"message":{"content":"lo"}}\n',
        b'{"done":true}\n',
    ])
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: response)
    provider = OllamaProvider("http://127.0.0.1:11434", "test")
    assert "".join(provider.chat([ChatMessage("user", "hi")])) == "Hello"


def test_invalid_json_is_controlled_error(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: FakeResponse([b"not-json\n"]))
    provider = OllamaProvider("http://127.0.0.1:11434", "test")
    with pytest.raises(LLMError, match="invalid JSON"):
        list(provider.chat([ChatMessage("user", "hi")]))


def test_http_404_becomes_provider_error(monkeypatch):
    def fail(*args, **kwargs):
        raise urllib.error.HTTPError("url", 404, "missing", {}, io.BytesIO(b'{"error":"model not found"}'))
    monkeypatch.setattr("urllib.request.urlopen", fail)
    provider = OllamaProvider("http://127.0.0.1:11434", "missing")
    with pytest.raises(LLMError, match="model not found"):
        list(provider.chat([ChatMessage("user", "hi")]))

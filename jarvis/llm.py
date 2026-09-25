from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterator, Sequence


class LLMError(RuntimeError):
    """Controlled provider error safe to show to the user."""


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"system", "user", "assistant", "tool"}:
            raise ValueError(f"Unsupported message role: {self.role}")
        if not isinstance(self.content, str):
            raise TypeError("Message content must be a string")


class LLMProvider:
    def chat(self, messages: Sequence[ChatMessage], *, stream: bool = True) -> Iterator[str]:
        raise NotImplementedError


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str, model: str, timeout: float = 120) -> None:
        if not model.strip():
            raise ValueError("Ollama model cannot be empty")
        if timeout <= 0:
            raise ValueError("Ollama timeout must be positive")
        self.base_url = base_url.rstrip("/")
        self.model = model.strip()
        self.timeout = timeout

    def _request(self, path: str, payload: dict) -> object:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            return urllib.request.urlopen(request, timeout=self.timeout)
        except urllib.error.HTTPError as exc:
            detail = self._http_error_detail(exc)
            if exc.code == 404:
                raise LLMError(f"Ollama endpoint/model not found: {detail}") from exc
            raise LLMError(f"Ollama HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise LLMError(f"Ollama unavailable: {exc}") from exc

    @staticmethod
    def _http_error_detail(exc: urllib.error.HTTPError) -> str:
        try:
            raw = exc.read().decode("utf-8", errors="replace")
            obj = json.loads(raw)
            return str(obj.get("error") or raw[:500])
        except Exception:
            return str(exc.reason or exc)

    def chat(self, messages: Sequence[ChatMessage], *, stream: bool = True) -> Iterator[str]:
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": stream,
        }
        response = self._request("/api/chat", payload)
        try:
            with response:
                if stream:
                    for raw in response:
                        if not raw.strip():
                            continue
                        yield self._parse_chunk(raw)
                else:
                    raw = response.read()
                    if not raw.strip():
                        raise LLMError("Ollama returned an empty response")
                    try:
                        obj = json.loads(raw)
                    except json.JSONDecodeError as exc:
                        raise LLMError("Ollama returned invalid JSON") from exc
                    if obj.get("error"):
                        raise LLMError(str(obj["error"]))
                    content = obj.get("message", {}).get("content")
                    if not isinstance(content, str):
                        raise LLMError("Ollama response did not contain message.content")
                    yield content
        except LLMError:
            raise
        except (TimeoutError, OSError) as exc:
            raise LLMError(f"Ollama response failed: {exc}") from exc

    @staticmethod
    def _parse_chunk(raw: bytes) -> str:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMError("Ollama returned invalid JSON") from exc
        if obj.get("error"):
            raise LLMError(str(obj["error"]))
        content = obj.get("message", {}).get("content", "")
        if not isinstance(content, str):
            raise LLMError("Ollama response contained invalid content")
        return content

    def health(self) -> bool:
        request = urllib.request.Request(self.base_url + "/api/tags", method="GET")
        try:
            with urllib.request.urlopen(request, timeout=5):
                return True
        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    def models(self) -> list[str]:
        request = urllib.request.Request(self.base_url + "/api/tags", method="GET")
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                data = json.load(response)
        except urllib.error.HTTPError as exc:
            raise LLMError(f"Ollama model discovery failed: HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise LLMError(f"Could not read Ollama models: {exc}") from exc
        models = data.get("models", [])
        if not isinstance(models, list):
            raise LLMError("Ollama returned an invalid model list")
        return [m["name"] for m in models if isinstance(m, dict) and isinstance(m.get("name"), str)]

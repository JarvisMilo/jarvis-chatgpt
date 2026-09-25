from __future__ import annotations

import platform
import sys
from pathlib import Path

from .config import Settings
from .llm import LLMProvider, OllamaProvider, LLMError
from .memory import MemoryRepository
from .tools import default_tools


def self_test(settings: Settings, provider: LLMProvider | None = None) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    results.append(("Python", "PASS" if sys.version_info >= (3, 11) else "FAIL"))
    results.append(("Platform", "PASS" if platform.system() == "Windows" else "WARN: Windows-first project"))
    results.append(("Workspace", "PASS" if settings.workspace.exists() else "FAIL"))
    results.append(("Memory", _memory_check(settings.db_path)))
    results.append(("Tool registry", _tool_check(settings.workspace)))

    if not isinstance(provider, OllamaProvider):
        provider = OllamaProvider(settings.ollama_base_url, settings.ollama_model, settings.ollama_timeout)

    healthy = provider.health()
    results.append(("Ollama service", "PASS" if healthy else "FAIL: service unavailable"))
    if healthy:
        try:
            models = provider.models()
            if settings.ollama_model in models:
                results.append(("Configured model", "PASS"))
            else:
                results.append(("Configured model", "FAIL: model not installed"))
        except LLMError as exc:
            results.append(("Model discovery", f"FAIL: {exc}"))
    else:
        results.append(("Configured model", "BLOCKED: Ollama unavailable"))

    return results


def _memory_check(path: Path) -> str:
    try:
        repo = MemoryRepository(path)
        item = repo.save("self-test", "ok")
        return "PASS" if repo.get(item.id) is not None else "FAIL"
    except Exception as exc:
        return f"FAIL: {type(exc).__name__}"


def _tool_check(workspace: Path) -> str:
    try:
        registry = default_tools(workspace)
        result = registry.execute("ping")
        return "PASS" if result["success"] and result["data"] == "pong" else "FAIL"
    except Exception as exc:
        return f"FAIL: {type(exc).__name__}"


def status(settings: Settings) -> dict[str, str]:
    provider = OllamaProvider(settings.ollama_base_url, settings.ollama_model, settings.ollama_timeout)
    return {
        "provider": settings.llm_provider,
        "model": settings.ollama_model,
        "ollama": "available" if provider.health() else "unavailable",
        "workspace": str(settings.workspace),
        "qa_mode": str(settings.qa_mode).lower(),
    }

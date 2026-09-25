from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    llm_provider: str
    ollama_base_url: str
    ollama_model: str
    ollama_timeout: float
    log_level: str
    db_path: Path
    workspace: Path
    qa_mode: bool


def load_settings() -> Settings:
    _load_dotenv()
    try:
        timeout = float(os.getenv("OLLAMA_TIMEOUT", "120"))
    except ValueError as exc:
        raise ValueError("OLLAMA_TIMEOUT must be a number") from exc
    if timeout <= 0:
        raise ValueError("OLLAMA_TIMEOUT must be positive")

    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip().rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "llama3.2").strip()
    if provider != "ollama":
        raise ValueError("Only Ollama is implemented in Level 1")
    if not base_url:
        raise ValueError("OLLAMA_BASE_URL cannot be empty")
    if not model:
        raise ValueError("OLLAMA_MODEL cannot be empty")

    settings = Settings(
        llm_provider=provider,
        ollama_base_url=base_url,
        ollama_model=model,
        ollama_timeout=timeout,
        log_level=os.getenv("JARVIS_LOG_LEVEL", "INFO").upper(),
        db_path=Path(os.getenv("JARVIS_DB_PATH", "data/jarvis.db")),
        workspace=Path(os.getenv("JARVIS_WORKSPACE", "workspace")),
        qa_mode=os.getenv("JARVIS_QA_MODE", "0").lower() in {"1", "true", "yes"},
    )
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    settings.workspace.mkdir(parents=True, exist_ok=True)
    return settings

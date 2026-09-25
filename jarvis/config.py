from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

def _load_dotenv() -> None:
    p = Path(".env")
    if not p.exists():
        return
    for raw in p.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k,v=line.split("=",1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

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
    s=Settings(
        llm_provider=os.getenv("LLM_PROVIDER","ollama").lower(),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL","http://127.0.0.1:11434").rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL","llama3.2"),
        ollama_timeout=float(os.getenv("OLLAMA_TIMEOUT","120")),
        log_level=os.getenv("JARVIS_LOG_LEVEL","INFO").upper(),
        db_path=Path(os.getenv("JARVIS_DB_PATH","data/jarvis.db")),
        workspace=Path(os.getenv("JARVIS_WORKSPACE","workspace")),
        qa_mode=os.getenv("JARVIS_QA_MODE","0").lower() in {"1","true","yes"},
    )
    s.db_path.parent.mkdir(parents=True,exist_ok=True)
    s.workspace.mkdir(parents=True,exist_ok=True)
    return s

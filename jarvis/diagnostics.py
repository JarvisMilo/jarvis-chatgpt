from __future__ import annotations
import importlib.util,platform,sys
from .config import Settings
from .llm import OllamaProvider

def self_test(settings:Settings)->list[tuple[str,str]]:
    out=[("Python","PASS" if sys.version_info>=(3,11) else "FAIL"),
         ("Platform","PASS" if platform.system()=="Windows" else "WARN"),
         ("Workspace","PASS" if settings.workspace.exists() else "FAIL")]
    if settings.llm_provider!="ollama":
        out.append(("LLM provider","FAIL: only Ollama is implemented in Level 1"))
        return out
    p=OllamaProvider(settings.ollama_base_url,settings.ollama_model,settings.ollama_timeout)
    healthy=p.health()
    out.append(("Ollama service","PASS" if healthy else "FAIL"))
    if healthy:
        try:
            models=p.models()
            out.append(("Configured model","PASS" if settings.ollama_model in models else "WARN: model not installed"))
        except Exception as e: out.append(("Model discovery",f"FAIL: {e}"))
    out.append(("pytest","LIVE_CHECK_REQUIRED"))
    return out

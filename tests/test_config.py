from jarvis.config import load_settings

def test_defaults(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    for name in ("LLM_PROVIDER","OLLAMA_BASE_URL","OLLAMA_MODEL","OLLAMA_TIMEOUT","JARVIS_DB_PATH","JARVIS_WORKSPACE"):
        monkeypatch.delenv(name, raising=False)
    settings = load_settings()
    assert settings.llm_provider == "ollama"
    assert settings.ollama_base_url == "http://127.0.0.1:11434"
    assert settings.ollama_model == "llama3.2"
    assert settings.workspace.exists()

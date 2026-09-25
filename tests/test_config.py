from jarvis.config import load_settings

def test_defaults(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path)
    s=load_settings()
    assert s.llm_provider=="ollama"
    assert s.ollama_base_url=="http://127.0.0.1:11434"
    assert s.workspace.exists()

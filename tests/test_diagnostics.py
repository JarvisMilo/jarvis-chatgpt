from jarvis.config import load_settings
from jarvis.diagnostics import self_test


def test_self_test_without_ollama_reports_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings = load_settings()
    results = dict(self_test(settings))
    assert results["Python"] == "PASS"
    assert results["Memory"] == "PASS"
    assert "Ollama service" in results

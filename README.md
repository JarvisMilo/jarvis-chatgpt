# JARVIS Local

A local-first personal agent for Windows, powered by Ollama. Level 1 focuses on a small, testable core: configuration, Ollama provider, streaming chat, context, SQLite memory, a secure tool registry, logging, CLI, and self-test.

## Requirements
- Python 3.11+
- Ollama installed locally
- A local Ollama model configured in `.env` or environment variables

## Quick start
```powershell
python -m jarvis --self-test
python -m jarvis
```

Set `OLLAMA_MODEL` to a model installed in Ollama.

## Architecture
User -> Core -> Context -> LLMProvider -> ToolRegistry -> tools -> result -> Core.

The LLM never receives direct operating-system access. Tools are explicit, registered, validated, and policy-gated.

See `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`, and `docs/PROGRESS.md`.

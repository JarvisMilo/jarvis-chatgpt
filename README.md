# JARVIS Local

Local-first personal assistant for Windows, using Ollama as the Level 1 LLM provider.

## Level 1

Implemented:

- centralized configuration
- provider abstraction with OllamaProvider
- chat and JSONL streaming
- controlled Ollama connection, HTTP, timeout and invalid-response errors
- separate conversation context
- SQLite memory with save/get/list/update
- explicit ToolRegistry with schema validation and risk gates
- safe ping and workspace-contained filesystem listing
- structured tool results
- CLI, self-test, status, doctor and version commands
- logging
- automated tests and GitHub Actions CI

No paid API is required. There is no OpenAI, Gemini or Anthropic runtime dependency.

## Requirements

- Python 3.11+
- Ollama installed locally
- at least one local Ollama model
- Windows is the primary target

## Setup

PowerShell:

    git clone https://github.com/JarvisMilo/jarvis-chatgpt.git
    cd jarvis-chatgpt
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -e ".[dev]"
    Copy-Item .env.example .env

Set OLLAMA_MODEL in .env to a model already installed in Ollama.

## Commands

    jarvis
    jarvis --self-test
    jarvis --status
    jarvis --doctor
    jarvis --version

Equivalent:

    python -m jarvis

Self-test performs live checks against the local Ollama service and configured model. It is expected to fail when Ollama is unavailable or the configured model is absent.

## Architecture

    User -> CLI -> JarvisCore -> ConversationContext -> LLMProvider -> OllamaProvider -> Ollama

Tools are explicit and registered. The LLM has no direct shell or operating-system execution primitive. Filesystem access in Level 1 is limited to the configured JARVIS workspace.

See docs/ARCHITECTURE.md and docs/SECURITY.md.

# JARVIS Local

Local-first personal assistant for Windows using Ollama. The repository is being developed as a cumulative six-level system: core intelligence, multi-agent orchestration, Windows control, local voice/vision, advanced intelligence, and an ambient full-assistant experience.

## Current state

The codebase contains the Level 1 core and executable foundations for Levels 2-6. These foundations include 15 agent specifications, orchestration primitives, Windows adapters, local voice/vision interfaces and an ambient HUD. They are deliberately separated so unfinished integrations cannot masquerade as completed capabilities.

**The project is not yet declared production-complete.** Live Windows hardware, Ollama, audio, vision, GUI automation and end-to-end acceptance tests still have to be performed on the target machine.

## Free/local architecture

- Ollama is the LLM provider; no paid API is required.
- Core logic does not directly execute arbitrary shell strings.
- Tool permissions and risk gates remain explicit.
- Voice and vision use replaceable local engine interfaces.
- The HUD is a presentation layer; it does not own business logic.

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

## Architecture

    User -> Context -> Ollama -> Planner/Orchestrator -> Permission Broker -> Tools/Agents -> Observation -> Verification -> Memory -> User

See docs/ARCHITECTURE.md, docs/AGENTS.md, docs/TOOLS.md, docs/SECURITY.md and docs/PROGRESS.md.

# Progress

CURRENT_LEVEL: 1
CURRENT_PHASE: Initial Level 1 implementation
STATUS: IN_PROGRESS

## Completed
- Repository initialized with a minimal Level 1 architecture.
- Central configuration.
- Ollama provider abstraction with streaming.
- SQLite basic memory repository.
- Tool registry with risk/confirmation gate.
- CLI and self-test.
- Initial unit tests.
- Architecture/roadmap documentation.

## In progress
- Verify the repository on the user's Windows machine.
- Verify Ollama/model availability and run the test suite.

## Next
- Run `python -m pytest`.
- Run `python -m jarvis --self-test`.
- Run a real Ollama chat.
- Fix verified failures only.

## Blockers
- Hardware, installed Python, Ollama service and installed models cannot be verified from GitHub alone.

## Known issues
- Tool calling from the model is intentionally not implemented yet.
- Memory retrieval is recent-only in Level 1.
- Windows-specific tools are deferred to Level 3.

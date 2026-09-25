# Progress

CURRENT_LEVEL: 1
CURRENT_PHASE: Verification
STATUS: IN_PROGRESS

## Permanent project target

docs/CAPABILITY_MATRIX.md is now the authoritative checklist for the complete
JARVIS target. It records the required capabilities, planned level, status,
future module/interface, dependencies and test strategy.

The matrix is broader than Level 1 by design. It prevents future capabilities
from being lost while keeping current implementation scope controlled.

## Implemented in repository

- central configuration and .env.example
- provider abstraction and OllamaProvider
- chat, non-streaming parsing and streaming JSONL
- controlled connection, HTTP, timeout and invalid-response errors
- separate ConversationContext
- SQLite memory save/get/list/update
- ToolRegistry with definitions, schema validation, risk levels and confirmation
- safe ping and workspace-contained listing tools
- structured tool results
- CLI: jarvis, --self-test, --status, --doctor, --version
- logging
- automated tests
- Windows GitHub Actions test workflow
- Level 1 documentation
- complete capability matrix for the six-level target
- Level 1 architecture updated with future extension boundaries

## Repository verification

- main is the default branch.
- repository is public and writable by the connected account.
- latest code is committed on main.
- pyproject.toml has no paid LLM runtime dependency.
- no OpenAI/Gemini/Anthropic runtime dependency exists.
- .env and generated data/workspace are ignored.
- GitHub Actions workflow is present, but no run/status is available yet for the latest commit.

## Not yet verified

These require execution on the actual runtime machine:

- installed Python
- local Ollama service
- configured model
- model capabilities
- real streamed conversation
- Windows CLI invocation
- final automated test run
- latest GitHub Actions result

## Level 1 remaining work

Before Level 1 can be declared complete:

1. inspect and harden any remaining Level 1 code defects.
2. verify automated tests on a real Windows/Python environment.
3. verify Ollama is reachable and the configured model exists.
4. verify a real streamed conversation.
5. verify memory persistence and safe workspace tool behavior.
6. verify controlled failures and self-test.
7. verify security boundaries and logs.
8. record exact results in this file.
9. stop at Level 1 and wait for explicit authorization before Level 2.

## Completion gate

Do not mark Level 1 complete until automated tests pass and a real local Ollama
conversation, streaming, memory, safe tool execution, error handling and
self-test have been verified.

## Intentional limits

- no autonomous tool calling/planning
- no shell execution
- no full Windows control
- no browser, audio or vision
- recent-only memory retrieval

NO LEVEL 2 WORK HAS STARTED.

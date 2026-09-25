# Test Plan — Level 1

Automated:
- configuration
- context trimming/message assembly
- memory CRUD
- Ollama JSONL parsing and HTTP errors
- tool registration/duplicate/unknown detection
- schema validation and confirmation
- workspace path containment
- Core streaming with fake provider
- CLI version

Live/manual:
- jarvis --self-test
- jarvis --status
- Ollama health
- configured model discovery
- real streamed conversation
- memory persistence across restarts
- safe workspace tool
- provider errors with service stopped and missing model

Security:
- no shell executor
- unknown tools rejected
- sensitive/dangerous/external-side-effect tools require confirmation
- workspace paths cannot escape the workspace
- generated data and .env are ignored
- external content is data, not authorization

Exit criteria:
All automated tests pass, the final CI run is green, and live/manual checks pass on the Windows machine.

# Test Plan — Level 1

## Unit
- configuration defaults
- memory save/retrieve
- tool registration
- duplicate-tool rejection
- confirmation enforcement

## Integration / manual
- Ollama health
- configured model discovery
- streamed response
- startup/shutdown behavior

## Security
- unknown tools rejected
- dangerous tools require confirmation
- no shell execution in Level 1
- no external communication tools in Level 1

## Exit criteria
All automated tests pass and the self-test accurately reports the real Ollama/model state.

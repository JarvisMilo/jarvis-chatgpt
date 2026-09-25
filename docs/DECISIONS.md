# Decisions

- Ollama is the only implemented LLM provider in Level 1.
- Provider code is isolated behind LLMProvider.
- Standard-library HTTP avoids an unnecessary runtime dependency.
- SQLite is used for persistent local memory.
- Conversation context and persistent memory remain separate.
- Tools are explicit, schema-validated and risk-classified.
- Tool metadata is exposed to the model as data, but autonomous tool calling is deferred.
- Filesystem access is limited to the configured workspace through a safe tool.
- No shell execution or external communication exists in Level 1.
- Windows is the primary target; platform-specific features are deferred.
- No paid API or secret is required.

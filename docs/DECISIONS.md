# Decisions

- Ollama is the only implemented LLM provider in Level 1.
- Standard-library HTTP is used for Ollama to avoid an unnecessary runtime dependency.
- SQLite is used for local memory.
- OS access is mediated by an explicit ToolRegistry.
- Level 1 remains text/CLI-first; UI and agent autonomy come later.
- No paid API or secret is required.

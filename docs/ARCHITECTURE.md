# Architecture — Level 1

Level 1 is intentionally text-first and modular.

    User
      -> CLI
      -> JarvisCore
      -> ConversationContext
      -> LLMProvider
      -> OllamaProvider
      -> local Ollama

    JarvisCore
      -> MemoryRepository (SQLite)
      -> ToolRegistry
           -> explicit safe tools

Boundaries:

- config.py: centralized configuration.
- context.py: short-lived conversation context and tool-result context.
- llm.py: provider contract plus Ollama implementation.
- memory.py: persistent local memory; separate from conversation history.
- tools.py: explicit metadata, schema validation, risk classification and confirmation.
- core.py: orchestration.
- cli.py: terminal interface.

The LLM has no direct OS primitive. Level 1 has no shell executor, browser automation, Windows control, autonomous planner or external communication.

ToolRegistry.definitions() exposes structured tool metadata to Core as context data. Autonomous tool selection/execution is deferred to the agent layer.

Data flow:
1. User sends text.
2. Core adds it to context.
3. Core retrieves a small recent memory slice.
4. Core exposes tool metadata as data.
5. Provider streams the model response.
6. Core appends only a successful assistant response.
7. Explicit application tool calls return structured results.

# Architecture — Level 1

Level 1 is intentionally text-first and modular, but its contracts are designed
for the complete six-level JARVIS architecture. The permanent target is tracked
in docs/CAPABILITY_MATRIX.md.

    User
      -> Interface Adapter
      -> JarvisCore
      -> ConversationContext
      -> LLMProvider
      -> OllamaProvider
      -> local Ollama

    JarvisCore
      -> MemoryRepository
      -> ToolRegistry
      -> future Agent/Policy/Task contracts

Future high-level flow:

    User
      -> Core
      -> Context/Awareness
      -> LLM Provider
      -> Intent/Plan
      -> Policy
      -> Permission/Confirmation
      -> Tool Dispatcher
      -> Tool Executor
      -> Verification
      -> Context/Memory
      -> Response

The future flow is architectural intent only. Level 1 does not implement the
planner, executor, Windows automation, browser, voice, vision, proactive
scheduler, research agent or remote/communications surfaces.

## Boundaries

- config.py: centralized configuration.
- context.py: short-lived conversation context and tool-result context.
- llm.py: provider contract plus Ollama implementation.
- memory.py: persistent local memory; separate from conversation history.
- tools.py: explicit metadata, schema validation, risk classification and confirmation.
- core.py: orchestration.
- cli.py: terminal interface.

Future contracts must remain outside these Level 1 modules where practical:

- agent/task system: planning, execution, retries, cancellation, recovery and verification.
- Windows adapter: OS/application/input/system control.
- browser adapter: controlled browser automation.
- perception adapters: screen, camera, OCR and vision models.
- voice adapters: STT, TTS, wake word, devices and interruption.
- awareness: dynamic hardware, tools, plugins, configuration and capability state.
- research: web retrieval, sources and provenance.
- documents: file/document parsing and artifact generation.
- development sandbox: code execution, tests and Git operations.
- plugins: discovery, metadata, permissions and isolation.
- proactive scheduler: reminders, background monitoring and notifications.
- UI/remote adapters: desktop HUD/dashboard and authenticated remote access.
- communications/media adapters: optional external communication and media control.

The LLM has no direct OS primitive. Level 1 has no shell executor, browser
automation, Windows control, autonomous planner or external communication.

ToolRegistry.definitions() exposes structured tool metadata to Core as context
data. Autonomous tool selection/execution is deferred to the agent layer.

## Extensibility rules

1. New levels extend Level 1 contracts; they do not replace them.
2. Every tool uses the same metadata, schema, risk and confirmation model.
3. Persistent memory remains behind a repository/service boundary.
4. UI and device adapters must not be embedded into JarvisCore.
5. External content is data, not authority.
6. Future capabilities must be registered in docs/CAPABILITY_MATRIX.md.
7. A capability that cannot yet be implemented receives a documented interface,
   dependency, local alternative, risk and test strategy rather than being removed.
8. Each level must preserve the previous level's regression tests.

## Level 1 data flow

1. User sends text.
2. Core adds it to context.
3. Core retrieves a small recent memory slice.
4. Core exposes tool metadata as data.
5. Provider streams the model response.
6. Core appends only a successful assistant response.
7. Explicit application tool calls return structured results.

# UI Architecture

The final interface is an ambient assistant surface, not a conventional dashboard or ChatGPT clone.

Core remains usable without UI. UI consumes events/state and requests actions through the same policy-controlled interfaces as other clients.

## State visualization

OFFLINE, STARTING, READY, SLEEPING, LISTENING, THINKING, PLANNING, EXECUTING, WAITING_PERMISSION, VERIFYING, SPEAKING, RECOVERING, ERROR and SHUTTING_DOWN must have visual representation when the UI is implemented.

The future UI may use an orb/core, waveform, contextual panels and transient activity views. Design is original and must not copy a reference project's interface.

A show-me-what-you-are-doing view may expose task/agent/tool progress but must redact secrets and sensitive values.

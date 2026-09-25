# Mark-LIV Functional Parity Plan

JARVIS uses Mark-LIV as a major functional reference while remaining an
independent implementation. Mark-LIV is licensed CC BY-NC 4.0, so JARVIS does
not copy its source code, UI assets, prompts, or implementation wholesale.

## Goal

Reproduce the useful capabilities in an original local-first architecture:

User -> Context -> Ollama -> Planner -> Orchestrator -> Permission Broker ->
Tool Router -> Agents/Adapters -> Observation -> Verification -> Recovery ->
Memory -> UI/Voice.

## Capability groups

- Voice: push-to-talk, wake word, local STT/TTS, interruption, echo protection,
  audio-device selection and silent mode.
- Perception: screenshot awareness, OCR, webcam input, UI/accessibility context
  and local vision models.
- Computer control: application discovery, launch/open, window management,
  keyboard/mouse, clipboard, system settings, media and browser control.
- Intelligence: persistent memory, recall, session continuity, proactive
  monitoring, reminders, research, code assistance and self-awareness.
- UX: ambient HUD, avatar/status visualization, content/activity panels,
  settings, theming and voice/audio controls.
- Extensibility: self-describing actions, plugin discovery and capability
  inspection.
- Operations: undo/action journal, confirmations, diagnostics, autostart,
  remote gateway and authenticated integrations.

## Local-first substitutions

| Reference function | JARVIS direction |
|---|---|
| Cloud conversational model | OllamaProvider |
| Cloud/live voice | local STT + local TTS adapters |
| Cloud vision | local vision model through Ollama or another local adapter |
| Cloud search | explicit web adapter; results are untrusted data |
| Cloud messaging | optional official/local adapters, always permission-gated |

No paid API key is required by the core runtime.

## Current bulk implementation

The runtime now has a foundation for reference-style self-describing actions
and plugins. Actions remain behind the existing Tool schema/risk contract;
high-risk execution passes through PermissionBroker and successful execution
is recorded in ActionJournal.

This is a functional parity program, not a claim that every Mark-LIV feature
is already implemented.

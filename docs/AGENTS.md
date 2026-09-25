# Agents Architecture

This document defines the real agent contracts for future levels. Level 1 does not implement the agent runtime; it preserves the boundaries required to add it without replacing Core.

## Mandatory agents

| Agent | Mission | Planned level | Status |
|---|---|---:|---|
| Orchestrator | Own objective lifecycle, delegation, dependencies and completion | 2 | PLANNED |
| Planner | Convert objectives into bounded steps and success criteria | 2 | PLANNED |
| Computer Control | Windows/apps/windows/input/process/system actions | 3 | PLANNED |
| File System | Search/read/write/move/copy/rename/delete/organize/undo | 3 | PLANNED |
| Browser | Controlled navigation, interaction, extraction and verification | 3 | PLANNED |
| Research | Multi-step research, sources and synthesis | 5 | PLANNED |
| Coding | Code analysis/edit/test/debug in a sandbox | 5 | PLANNED |
| Git/DevOps | Git, CI, builds, release and recovery | 5 | PLANNED |
| Vision | Screenshots, OCR, visual grounding and camera | 4 | PLANNED |
| Voice | STT/TTS, wake, VAD, interruption and devices | 4 | PLANNED |
| Memory | Retrieval, update, compression, deduplication and lifecycle | 2→5 | PLANNED |
| System Monitor | Hardware, processes, health and alerts | 3→5 | PLANNED |
| Automation | Schedules, workflows and background execution | 5 | PLANNED |
| Security/Policy | Risk, permissions, confirmation, sandbox and audit | 2→6 | PLANNED |
| QA/Verification | Verify effects, tests, results and recovery triggers | 2→6 | PLANNED |

## Agent contract

Every real agent must declare identity, mission, input schema, output schema, allowed tools, permissions, memory scope, limits, timeout, cancellation behavior, error strategy, reporting events and tests.

An agent is not implemented because a class exists. It must execute or coordinate its declared responsibility through real contracts and tests.

## Orchestration rules

- Agents receive bounded tasks, not arbitrary OS access.
- The Orchestrator owns task lifecycle; specialized agents own domain work.
- Parallel execution is allowed only for independent and policy-approved tasks.
- Mutating tasks are serialized unless policy explicitly proves safe concurrency.
- Every task has cancellation, timeout, retry and verification semantics.
- Agent output is untrusted data until verified where side effects are involved.
- Security/Policy cannot be bypassed by another agent.
- QA/Verification can reject an unverified success.
- Background tasks persist state and emit progress events.

## Shared state

Agents communicate through Events, Tasks, Observations, ToolResults and typed Context. They do not directly modify another agent's private state.

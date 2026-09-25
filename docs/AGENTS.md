# JARVIS Agent Team

JARVIS has a concrete team of 20 specialized agents. Each has a mission, capability set and execution contract. Agents receive structured data only; they never receive arbitrary OS handles.

| # | Agent | Mission |
|---:|---|---|
| 1 | Orchestrator | lifecycle and coordination |
| 2 | Planner | decomposition and verification planning |
| 3 | Computer Control | approved Windows interaction |
| 4 | File System | filesystem and document operations |
| 5 | Browser | browser automation and extraction |
| 6 | Research | web research and provenance |
| 7 | Coding | local software development |
| 8 | Git DevOps | repository and CI workflows |
| 9 | Vision | screenshots, OCR and visual observations |
| 10 | Voice | local STT/TTS/wake coordination |
| 11 | Memory | recall, update and forget |
| 12 | System Monitor | resources and health |
| 13 | Automation | schedules, reminders and notifications |
| 14 | Security Policy | risk and permission evaluation |
| 15 | QA Verification | outcome verification and recovery |
| 16 | Media | media playback/search/control |
| 17 | Communications | external messaging adapters |
| 18 | Presentation | document/presentation artifacts |
| 19 | Personalization | identity/UI/preferences |
| 20 | Remote Gateway | authenticated remote boundary |

The LLM proposes intent. Runtime code chooses an allowed agent/tool, applies policy, executes and verifies the result. Agent count is deliberately above the required minimum of 15.

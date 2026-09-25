# Capability Matrix — JARVIS

This matrix is the permanent checklist for the complete JARVIS target.
Level 1 implements only its defined foundation. Future capabilities are
recorded now so later levels extend the architecture without replacing it.

Status values: PLANNED, IN_PROGRESS, IMPLEMENTED, TESTED, BLOCKED.

## Reference basis

The matrix consolidates the capability inventory defined for this project and
the architectural/function ideas identified from public JARVIS/AI-assistant
references, including:

- FatihMakes/Mark-LIV
- msxfury/JARVIS-Mark-LI
- MAL19INDUSTRIES/JARVIS-OS-V.2
- earlier Mark-X / Mark variants considered during project planning

This project is an independent implementation. No reference project's code is
being copied or forked.

## Capability matrix

| Capacidad | Proyecto de referencia | ¿JARVIS la tendrá? | Nivel | Estado | Módulo / interfaz prevista |
|---|---|---:|---:|---|---|
| Ollama/local LLM brain | Mark/variants; project requirement | Sí | 1 | IN_PROGRESS | llm.LLMProvider / OllamaProvider |
| Local model selection | Mark/variants | Sí | 1 | IN_PROGRESS | config / llm |
| Streaming conversation | Mark/variants | Sí | 1 | IN_PROGRESS | llm / core / UI-voice adapters |
| Natural conversation + history | All references | Sí | 1 | IN_PROGRESS | context / core / conversation store |
| Context compression / long conversations | Mark/variants | Sí | 2 | PLANNED | context / compression |
| Interruption / cancel current response | Voice/agent assistants | Sí | 4 | PLANNED | runtime / voice / tasks |
| Language detection / language switching | Assistant references | Sí | 4 | PLANNED | language / voice / context |
| Configurable personality and identity | All references | Sí | 1→5 | IN_PROGRESS | config / core / identity profile |
| Runtime self-knowledge / capability awareness | JARVIS-Mark-LI; project requirement | Sí | 5 | PLANNED | awareness / capability registry |
| Text responses | All references | Sí | 1 | IN_PROGRESS | cli / future UI |
| Voice responses | Mark-LI / JARVIS OS | Sí | 4 | PLANNED | voice.tts |
| Silent mode | Voice assistants | Sí | 4 | PLANNED | voice/runtime |
| Persistent conversation history | JARVIS OS / assistant systems | Sí | 1→5 | PLANNED | conversation repository |
| Short-term memory | All agent architectures | Sí | 1→2 | IN_PROGRESS | context |
| Session memory | Agent architectures | Sí | 1→2 | PLANNED | context / session store |
| Long-term memory | Mark-LI / JARVIS OS | Sí | 5 | PLANNED | memory |
| Project memory | Agent/developer assistants | Sí | 5 | PLANNED | memory.projects |
| User preferences / important facts | All assistant architectures | Sí | 5 | PLANNED | memory |
| Task history | Agent systems | Sí | 2 | PLANNED | tasks.history |
| System awareness/context | Mark-LI / JARVIS OS | Sí | 3→5 | PLANNED | awareness / system adapters |
| Persistent local storage | All references | Sí | 1 | IN_PROGRESS | SQLite repositories |
| Semantic/local memory search | Agent assistants | Sí | 5 | PLANNED | local index / embeddings adapter |
| On-demand memory retrieval | Agent assistants | Sí | 2→5 | PLANNED | memory.retrieval |
| Memory update/delete/inspection | Project requirement | Sí | 1→5 | IN_PROGRESS | memory.MemoryRepository |
| Duplicate prevention / context budgeting | Project requirement | Sí | 2→5 | PLANNED | memory / context |
| Memory summarization/compression | Agent assistants | Sí | 2→5 | PLANNED | compression / memory |
| Task object/state machine | Agent architectures | Sí | 2 | PLANNED | tasks |
| Task queue | Agent architectures | Sí | 2 | PLANNED | tasks.queue |
| Planner | Agent architectures | Sí | 2 | PLANNED | agent.planner |
| Executor | Agent architectures | Sí | 2 | PLANNED | agent.executor |
| Tool dispatcher | Agent architectures | Sí | 2 | PLANNED | tools.dispatcher |
| Retry / replan / recovery | Agent architectures | Sí | 2 | PLANNED | agent.recovery |
| Cancellation / progress | Agent architectures | Sí | 2 | PLANNED | tasks.runtime |
| Result verification | Agent architectures | Sí | 2 | PLANNED | agent.verification |
| Modular tool registry | All references | Sí | 1 | IN_PROGRESS | tools.ToolRegistry |
| Tool schema validation | Agent architectures | Sí | 1 | IN_PROGRESS | tools |
| Risk / permission / confirmation model | Security requirement | Sí | 1→3 | IN_PROGRESS | tools / future security |
| Undo / reversibility | Agent/desktop automation requirement | Sí | 2→3 | PLANNED | undo / action journal |
| Plugin/skill discovery | JARVIS OS / assistant architectures | Sí | 5→6 | PLANNED | plugins |
| Plugin metadata/config/permissions/isolation | Project requirement | Sí | 5→6 | PLANNED | plugins / security |
| Windows application control | Mark-LIV / Mark variants | Sí | 3 | PLANNED | windows.apps |
| Window management | Mark-LIV / desktop assistants | Sí | 3 | PLANNED | windows.windows |
| Keyboard/mouse/desktop control | Mark-LIV / computer-use assistants | Sí | 3 | PLANNED | windows.input |
| Clipboard intelligence | Project requirement | Sí | 3 | PLANNED | windows.clipboard |
| Volume / brightness / Wi-Fi / Bluetooth | Desktop assistants | Sí | 3 | PLANNED | windows.system |
| Processes / terminal / PowerShell | Mark-LIV / desktop automation | Sí | 3 | PLANNED | windows.processes / controlled shell |
| CPU/RAM/GPU/VRAM/storage/network telemetry | JARVIS-Mark-LI / system assistants | Sí | 3 | PLANNED | hardware |
| Temperature/battery monitoring when available | Desktop/system assistants | Sí | 3 | PLANNED | hardware |
| Shutdown/restart/lock | Desktop assistants | Sí | 3 | PLANNED | windows.power |
| Browser automation | Mark-LIV / JARVIS OS | Sí | 3 | PLANNED | browser / Playwright adapter |
| Browser navigation/tabs/forms/downloads | JARVIS OS / computer-use assistants | Sí | 3 | PLANNED | browser |
| Browser result verification | Agent/browser automation | Sí | 3 | PLANNED | browser.verification |
| Screenshot capture | Mark-LIV / JARVIS OS | Sí | 4 | PLANNED | vision.screen |
| Screen understanding | Mark-LIV / vision assistants | Sí | 4 | PLANNED | vision / visual model adapter |
| Webcam/image input | Vision assistants | Sí | 4 | PLANNED | vision.camera |
| OCR/document vision | JARVIS OS / vision assistants | Sí | 4 | PLANNED | vision.ocr |
| Voice STT | Mark-LI / JARVIS OS | Sí | 4 | PLANNED | voice.stt |
| Local TTS | Mark-LI / JARVIS OS | Sí | 4 | PLANNED | voice.tts |
| Microphone/speaker selection | Voice assistants | Sí | 4 | PLANNED | voice.devices |
| Push-to-talk | Voice assistants | Sí | 4 | PLANNED | voice.input |
| Wake word / Hey JARVIS | Voice assistants | Sí | 4 | PLANNED | voice.wake |
| Sleep/wake state | Voice assistants | Sí | 4 | PLANNED | runtime.state |
| Self-echo protection | Voice assistants | Sí | 4 | PLANNED | voice.echo |
| Voice interruption/barge-in | Voice assistants | Sí | 4 | PLANNED | voice.interrupt |
| Voice while tasks execute | Agent + voice architecture | Sí | 4 | PLANNED | voice / tasks |
| Main desktop UI | JARVIS OS / Mark variants | Sí | 6 | PLANNED | ui |
| Chat / status / activity | JARVIS OS | Sí | 6 | PLANNED | ui.panels |
| Logs/history/tools/memory/task views | JARVIS OS / agent dashboards | Sí | 6 | PLANNED | ui.dashboard |
| Permissions / confirmation UI | Security architecture | Sí | 6 | PLANNED | ui.security |
| HUD / avatar / waveform / themes | Mark variants / JARVIS UI concepts | Sí | 6 | PLANNED | ui.hud / ui.avatar |
| Proactive reminders | Agent assistants | Sí | 5 | PLANNED | proactive / scheduler |
| Scheduled tasks | Agent assistants | Sí | 5 | PLANNED | scheduler |
| Notifications / morning briefing | JARVIS assistant concepts | Sí | 5 | PLANNED | proactive |
| Background monitoring | Agent/system assistants | Sí | 5 | PLANNED | monitoring |
| Web search | Mark-LI / JARVIS OS | Sí | 5 | PLANNED | research.web |
| News / price / multi-step research | Research assistants | Sí | 5 | PLANNED | research |
| Sources / extraction / verification | Research assistants | Sí | 5 | PLANNED | research.sources |
| Local vs web vs model knowledge provenance | Project requirement | Sí | 5 | PLANNED | provenance |
| TXT/MD/PDF/DOCX/XLSX/CSV/JSON support | JARVIS OS / productivity assistants | Sí | 5 | PLANNED | documents |
| Image/document analysis | Vision + document assistants | Sí | 5 | PLANNED | documents / vision |
| Document transformation/generation | JARVIS OS | Sí | 5→6 | PLANNED | documents / artifact layer |
| Code reading/explanation/generation | JARVIS-Mark-LI / developer assistants | Sí | 5 | PLANNED | dev_agent |
| Code modification/review/debugging | Developer agents | Sí | 5 | PLANNED | dev_agent / sandbox |
| Test/lint/build/log execution | Developer agents | Sí | 5 | PLANNED | dev_agent / sandbox |
| Git status/diff/branch/log/commit | Developer agents | Sí | 5 | PLANNED | dev.git |
| Git recovery/documentation | Developer agents | Sí | 5 | PLANNED | dev.git |
| Sandboxed development actions | Security requirement | Sí | 5 | PLANNED | sandbox / security |
| Safe grouped undo | Project requirement | Sí | 2→5 | PLANNED | undo |
| Prompt-injection defense | Security requirement | Sí | 1→5 | IN_PROGRESS | security / trust boundaries |
| Tool isolation / malicious-tool defense | Security requirement | Sí | 5→6 | PLANNED | security / plugin sandbox |
| Resource/time/loop limits | Agent security | Sí | 2→5 | PLANNED | policy / runtime |
| Audit logs | Security requirement | Sí | 1→6 | IN_PROGRESS | logging / audit store |
| Local secrets management | Security requirement | Sí | 3→6 | PLANNED | secrets |
| YouTube/media search/playback/control | Project requirement / media assistants | Sí | 3 | PLANNED | media |
| WhatsApp integration | Project requirement | Sí | 6 | PLANNED | communications |
| Telegram integration | Project requirement | Sí | 6 | PLANNED | communications |
| Email integration | Project requirement / JARVIS OS | Sí | 6 | PLANNED | communications.email |
| External communication confirmation | Security requirement | Sí | 6 | PLANNED | security / communications |
| Remote dashboard | Project requirement | Sí | 6 | PLANNED | remote |
| Remote authentication/pairing | Project requirement | Sí | 6 | PLANNED | remote.security |
| User/name/language/voice/appearance preferences | All references | Sí | 5→6 | PLANNED | preferences |
| Configurable permissions/tools | Project requirement | Sí | 3→6 | PLANNED | policy / preferences |
| Windows autostart | Desktop assistants | Sí | 6 | PLANNED | installer / autostart |
| Install/uninstall/recovery | Desktop product architecture | Sí | 6 | PLANNED | installer |
| Dynamic capability discovery | Project requirement | Sí | 5→6 | PLANNED | capability registry |
| Dynamic hardware/tool/plugin awareness | Project requirement | Sí | 3→6 | PLANNED | awareness |
| Non-regression across levels | Project architecture rule | Sí | 1→6 | IN_PROGRESS | CI + regression suite |

## Cross-level dependency rules

1. Level 1 owns stable contracts for configuration, LLM providers, context,
   memory repositories, tool metadata/risk, logging, errors and CLI.
2. Level 2 adds planning/orchestration without replacing Level 1 contracts.
3. Level 3 adds Windows/browser control behind tools, policy and permissions.
4. Level 4 adds perception/voice behind independent adapters.
5. Level 5 adds long-term intelligence, research, development and proactive
   systems.
6. Level 6 adds the complete product/UI/plugin/remote/communication surface.
7. Every new level must run the previous level's regression suite.
8. No future module may give the LLM direct OS access.
9. External content is data, not authority.
10. Difficult or unavailable technologies remain documented here and receive a
    stable interface before implementation.

## Level 1 architectural contracts that must remain extensible

- LLMProvider: future local model adapters can coexist without changing core
  orchestration.
- ConversationContext: future compression, interruption and awareness data
  must be addable without mixing persistent memory into chat history.
- MemoryRepository: future memory types/search/indexing must remain behind a
  repository/service boundary.
- Tool / ToolRegistry: future Windows, browser, vision, media and communication
  tools must use the same metadata/risk/permission contract.
- Settings: future configuration should be added centrally rather than
  hard-coded in modules.
- JarvisCore: should remain orchestration-focused; planners, executors, UI and
  device adapters must not become embedded in it.
- Logging/error contracts must support auditability and task recovery later.

## Technology readiness notes

| Future capability | Need | Local-first option | Risk / constraint | Planned interface | Test strategy |
|---|---|---|---|---|---|
| Local semantic memory | Embedding/indexing | Ollama embeddings + SQLite/vector index | Model/storage compatibility | MemoryIndex | deterministic fixture retrieval |
| Browser automation | Browser driver | Playwright | Website changes, credentials, side effects | BrowserAdapter | isolated test pages |
| STT | Speech model + audio I/O | whisper.cpp / faster-whisper/local model | CPU/GPU load, device access | STTProvider | prerecorded audio fixtures |
| TTS | Speech synthesis | Piper or another local TTS engine | voice/device compatibility | TTSProvider | generated-audio smoke tests |
| Wake word | Wake-word engine | openWakeWord or equivalent local engine | false positives/CPU | WakeWordProvider | audio fixtures |
| Vision | Vision-capable local model | Ollama vision model or local vision runtime | VRAM/model capability | VisionProvider | screenshot/image fixtures |
| OCR | OCR engine | Tesseract/PaddleOCR/local runtime | language/model setup | OCRProvider | fixture images |
| Windows automation | OS APIs | pywin32 / UI Automation / PowerShell under policy | high side-effect risk | WindowsAdapter | mocked + sandboxed live checks |
| Hardware telemetry | OS/vendor APIs | psutil + Windows/WMI/vendor APIs | sensor availability | HardwareProvider | capability-dependent tests |
| Documents | Parsers | stdlib + open-source format libraries as needed | parser/security limits | DocumentProvider | fixture corpus |
| Development agent | Sandbox + tools | local subprocess sandbox / containers where available | arbitrary code execution | DevExecutor | isolated projects |
| Remote dashboard | Authenticated local service | local HTTPS/FastAPI or equivalent | remote attack surface | RemoteGateway | auth/security tests |
| Communications | platform connectors | local/official clients where available | credentials/external side effects | CommunicationProvider | mocks; explicit live confirmation |
| Autostart | Windows startup integration | Task Scheduler/startup registration | persistence/install permissions | AutostartManager | install/uninstall tests |

## Source notes

The public reference repositories confirm the broad architectural direction:
Mark-LIV describes a computer-controlling AI model; JARVIS-Mark-LI describes
conversation, voice, computer vision, memory, desktop automation and system
control; JARVIS-OS-V.2 describes a desktop assistant with voice, UI and
optional browser/file/screen/messaging tools plus research and presentation
workflows. This project treats those as reference ideas, not as code to copy.

This matrix is deliberately broader than Level 1. A PLANNED entry is not a
promise that its implementation belongs in the current level.

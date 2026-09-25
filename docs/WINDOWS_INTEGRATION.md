# Windows Integration Architecture

Windows integration is Level 3+ and must remain behind explicit adapters and policy-controlled tools.

Application discovery → Application Registry → ApplicationAdapter → policy/permission → executor → observation → verification.

Discovery may use Start Menu, registry, PATH, Program Files, AppData, AppX/Microsoft Store metadata, shortcuts, protocols, file associations and running processes. The implementation must discover the actual machine rather than assume installed applications.

ApplicationAdapter should expose launch, close, focus, minimize, maximize, switch, inspect, state and interaction capabilities. Prefer official API/CLI, then protocol/deep link, automation API, GUI automation, vision+input, and finally assisted/manual fallback.

PowerShell/terminal access must be a controlled tool, never a raw LLM shell primitive.

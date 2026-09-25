# Installation Architecture

Installation is planned for Level 6. It must provide real install, start, stop, diagnose, update and uninstall operations rather than placeholder scripts.

Startup must support graceful degradation: missing optional voice, vision or browser capabilities must not prevent text/local Core from starting.

Autostart changes require explicit user authorization and must be reversible.

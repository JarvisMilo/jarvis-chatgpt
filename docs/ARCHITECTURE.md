# Architecture — Level 1

The core is deliberately small.

User -> CLI -> JarvisCore -> Context/history -> LLMProvider -> Ollama.

Tools are explicit objects in ToolRegistry. The model does not receive OS access; future agent layers will convert model intent into validated tool calls.

Memory is a separate SQLite repository. It is not the same thing as chat history, awareness, or task state.

Level 1 intentionally excludes browser automation, shell, Windows control, audio, vision, autonomous planning, and external communication.

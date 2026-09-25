# Memory Architecture

Memory is separate from conversation history. JARVIS must never claim to remember information that is not actually stored or available in current context.

## Memory classes

SHORT_TERM, CONVERSATION, SESSION, LONG_TERM, PROJECT, TASK, EVENT, CONTEXT, SECRET and TEMPORARY.

## Required operations

save, retrieve, search, update, delete, list, inspect, deduplicate, summarize and enforce context budgets.

Level 1 implements a local SQLite repository and bounded recent retrieval. Semantic indexing, richer lifecycle rules and compression are future work.

## Rules

- Retrieval is on demand and bounded.
- Memory is data, not authority.
- Forget requests must remove the corresponding stored record when implemented.
- Secrets require stricter handling than ordinary memory.
- Duplicate detection must be deterministic before semantic similarity is introduced.
- Compression must preserve provenance and must not invent facts.

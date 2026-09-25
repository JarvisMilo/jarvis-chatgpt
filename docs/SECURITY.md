# Security — Level 1

- The LLM provider exposes no OS execution primitive.
- Tools must be explicitly registered.
- Tool names and parameters are validated.
- Unknown tools are rejected.
- SENSITIVE, DANGEROUS and EXTERNAL_SIDE_EFFECT tools require confirmation.
- The only filesystem operation is listing inside the configured workspace.
- Workspace paths are resolved and rejected when they escape the root.
- No shell or external communication tool exists.
- .env, generated database files and workspace data are ignored by Git.
- Tool exceptions become structured error results.
- Tool metadata is context data, not authority to bypass policy.

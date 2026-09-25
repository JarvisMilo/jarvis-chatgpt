# Tools — Level 1 and Future Tool Contract

Every tool is explicit and policy-controlled.

## Tool contract

A tool declares:

- name
- description
- parameter schema
- validator
- permission
- risk
- timeout
- retry policy
- executor
- structured result
- reversibility/undo operation when possible
- verification strategy
- category

The LLM cannot call arbitrary Python, PowerShell, shell, OS APIs or plugin code.

## Level 1 implemented tools

| Tool | Risk | Confirmation | Scope |
|---|---|---|---|
| ping | SAFE | No | Local health-check |
| workspace_list | SAFE | No | Configured JARVIS workspace only |

Results use:

{success, data, error, warnings, artifacts}

Unknown tools are rejected. Invalid parameters are rejected. Tool exceptions become structured failures.

## Future tool families

Windows/application, filesystem, browser, screen/vision, voice/audio, hardware, documents, research/web, development/Git, automation/scheduler, clipboard/media, communications, plugins and remote-control tools will all use the same contract.

Destructive or external-side-effect tools require policy evaluation and human confirmation as configured. Critical actions may additionally require authentication.

## Discovery

Future plugins and application adapters may be discovered dynamically, but discovery never grants execution permission. Manifests, schemas, dependencies and permissions are validated before activation.

## Level boundaries

Level 1 deliberately has no shell, process-control, browser, general filesystem, Windows-control, network-side-effect or autonomous tool-calling capability.

# Development Agent Architecture

The future Coding and Git/DevOps agents operate in a controlled development sandbox.

Capabilities include repository inspection, code editing, tests, lint, build, logs, debugging, Git status/diff/branch/log/commit and documentation. Destructive operations require explicit authorization.

Generated code is data until validated. Arbitrary code execution is never exposed directly to the LLM; execution occurs through a policy-controlled sandbox/executor with timeouts and resource limits.

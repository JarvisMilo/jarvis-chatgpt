# Recovery Architecture

Failures are first-class results. A failed task should move through detect → diagnose → alternative strategy → retry/replan → verify → report.

Recovery must have bounded retries, timeouts and loop limits. It must never silently escalate permissions or modify security policy.

Undo is separate from recovery: an undo operation must use a recorded prior state/action, never an invented value.

Future Action Journal records safe action metadata, reversibility and an exact undo operation where possible.

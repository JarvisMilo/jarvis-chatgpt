# Security — Level 1

- The LLM provider has no direct OS execution primitive.
- Tools are registered explicitly.
- DANGEROUS and EXTERNAL_SIDE_EFFECT tools are confirmation-gated.
- No shell tool exists in Level 1.
- No secrets are committed; `.env` is ignored.
- QA mode is represented in configuration and will be enforced more deeply as agent/tool layers are added.

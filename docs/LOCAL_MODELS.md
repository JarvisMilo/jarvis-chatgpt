# Local Models

OLLAMA_MODEL is the single Level 1 model configuration point.

Example:

    OLLAMA_MODEL=llama3.2

The model must already be installed in the local Ollama service. JARVIS does not automatically download models.

Capabilities vary by model/version. Tool calling, structured output, vision and context limits are not assumed in Level 1.

Use:

    jarvis --self-test

to check whether the configured model is visible to Ollama.

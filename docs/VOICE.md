# Voice Architecture

Voice is a replaceable local-first adapter layer and must never become a hard dependency of Core.

Microphone → VAD/wake detector → STTProvider → input event → Core/Agent runtime → TTSProvider → speaker.

Planned local adapters include Whisper/faster-whisper/whisper.cpp for STT and Piper/Kokoro or another suitable local engine for TTS. Selection depends on real hardware, latency, model size, license and installation complexity.

Required future capabilities: device selection, push-to-talk, wake word, sleep/wake, clap activation, self-echo protection, barge-in/interruption, silent mode and graceful fallback to text.

No ElevenLabs, OpenAI TTS or paid cloud voice service is a required dependency.

from __future__ import annotations
from abc import ABC, abstractmethod

class STTEngine(ABC):
    @abstractmethod
    def transcribe(self,audio: bytes)->str: ...
class TTSEngine(ABC):
    @abstractmethod
    def synthesize(self,text: str)->bytes: ...
class VoiceManager:
    def __init__(self, stt:STTEngine|None=None, tts:TTSEngine|None=None): self.stt=stt; self.tts=tts

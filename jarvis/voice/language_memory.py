from __future__ import annotations
class LanguageMemory:
    def __init__(self,default="es"): self.language=default
    def set(self,language): self.language=language
    def get(self): return self.language

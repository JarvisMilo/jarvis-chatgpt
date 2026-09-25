from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
@dataclass
class VisualObservation:
    source:str; path:Path; description:str=""
class VisualAwareness:
    def __init__(self,capture): self.capture=capture
    def snapshot(self,path): return VisualObservation("screen",Path(path))

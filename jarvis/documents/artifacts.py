from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import uuid
@dataclass(frozen=True)
class Artifact: id:str; path:Path; kind:str
class ArtifactStore:
    def __init__(self,root): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def register(self,path,kind): return Artifact(str(uuid.uuid4()),Path(path),kind)

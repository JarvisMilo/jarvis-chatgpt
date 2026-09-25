from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class ModelProfile: name:str; roles:tuple[str,...]; min_ram_gb:float=0; min_vram_gb:float=0
class ModelRouter:
    def __init__(self,profiles=()): self.profiles=list(profiles)
    def choose(self,role,ram_gb=0,vram_gb=0,preferred=None):
        candidates=[p for p in self.profiles if role in p.roles and ram_gb>=p.min_ram_gb and vram_gb>=p.min_vram_gb]
        if preferred and any(p.name==preferred for p in candidates): return preferred
        return candidates[0].name if candidates else None

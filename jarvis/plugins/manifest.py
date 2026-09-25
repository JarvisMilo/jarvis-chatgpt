from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class PluginManifest:
    name:str; version:str; description:str=""; permissions:tuple[str,...]=(); tools:tuple[str,...]=(); dependencies:tuple[str,...]=()
    @classmethod
    def from_dict(cls,data): return cls(str(data["name"]),str(data.get("version","0")),str(data.get("description","")),tuple(data.get("permissions",())),tuple(data.get("tools",())),tuple(data.get("dependencies",())))

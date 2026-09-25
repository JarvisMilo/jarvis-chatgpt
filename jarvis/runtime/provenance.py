from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
class SourceKind(str,Enum): MODEL="MODEL"; LOCAL="LOCAL"; TOOL="TOOL"; WEB="WEB"; USER="USER"
@dataclass(frozen=True)
class Provenance:
    kind:SourceKind; label:str; trusted:bool=False
    def as_text(self): return f"[{self.kind.value}:{self.label}]"

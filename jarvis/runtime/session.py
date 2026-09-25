from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
import uuid
@dataclass
class Session:
    id:str=field(default_factory=lambda:str(uuid.uuid4())); started_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat()); turns:list[dict]=field(default_factory=list)
    def add(self,role,content): self.turns.append({"role":role,"content":content,"at":datetime.now(timezone.utc).isoformat()})
class SessionManager:
    def __init__(self): self.current=Session(); self.sessions=[self.current]
    def new(self): self.current=Session(); self.sessions.append(self.current); return self.current
    def recent(self,n=20): return self.current.turns[-n:]

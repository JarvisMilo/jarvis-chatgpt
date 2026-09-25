from __future__ import annotations
from dataclasses import dataclass
import uuid
@dataclass
class ConfirmationRequest:
    id:str; action:str; reason:str; risk:str; approved:bool=False
class ConfirmationManager:
    def __init__(self): self.pending={}
    def request(self,action,reason,risk):
        item=ConfirmationRequest(str(uuid.uuid4()),action,reason,risk); self.pending[item.id]=item; return item
    def approve(self,id):
        item=self.pending.get(id)
        if not item: return False
        item.approved=True; return True
    def consume(self,id):
        item=self.pending.pop(id,None); return bool(item and item.approved)

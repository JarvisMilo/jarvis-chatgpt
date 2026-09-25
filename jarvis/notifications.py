from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
@dataclass(frozen=True)
class Notification: title:str; message:str; created_at:str
class NotificationManager:
    def __init__(self): self.history=[]
    def push(self,title,message):
        item=Notification(title,message,datetime.now(timezone.utc).isoformat()); self.history.append(item); return item

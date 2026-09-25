from __future__ import annotations
from dataclasses import dataclass
@dataclass
class UndoEntry: description:str; undo:object
class UndoManager:
    def __init__(self): self.stack=[]
    def push(self,description,undo): self.stack.append(UndoEntry(description,undo))
    def undo(self):
        if not self.stack: return {"success":False,"reason":"EMPTY"}
        item=self.stack.pop(); item.undo(); return {"success":True,"description":item.description}

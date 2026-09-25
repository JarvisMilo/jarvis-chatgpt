from __future__ import annotations
from collections import deque
class EchoGuard:
    def __init__(self,max_items=40): self.tail=deque(maxlen=max_items)
    def remember_output(self,text): self.tail.append((text or "").lower())
    def filter(self,text):
        t=(text or "").strip()
        return "" if any(t.lower()==x for x in self.tail) else t

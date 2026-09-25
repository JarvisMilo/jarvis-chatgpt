from __future__ import annotations
from datetime import datetime,timezone
class AwarenessSnapshot:
    def __init__(self,**values): self.values=values; self.created_at=datetime.now(timezone.utc).isoformat()
    def as_dict(self): return {"created_at":self.created_at,**self.values}

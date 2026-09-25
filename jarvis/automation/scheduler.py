from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
import threading,uuid
@dataclass
class ScheduledJob: id:str; name:str; run_at:datetime; callback:object; enabled:bool=True
class LocalScheduler:
    def __init__(self): self.jobs={}; self._lock=threading.Lock()
    def schedule(self,name,run_at,callback):
        job=ScheduledJob(str(uuid.uuid4()),name,run_at,callback)
        with self._lock: self.jobs[job.id]=job
        return job
    def cancel(self,job_id):
        with self._lock:
            if job_id in self.jobs: self.jobs[job_id].enabled=False; return True
        return False
    def due(self,now=None):
        now=now or datetime.now(timezone.utc); return [j for j in self.jobs.values() if j.enabled and j.run_at<=now]

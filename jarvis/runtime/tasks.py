from __future__ import annotations
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from threading import Event as CancelEvent
from typing import Callable, Any

class TaskStatus(str, Enum): QUEUED="QUEUED"; RUNNING="RUNNING"; SUCCEEDED="SUCCEEDED"; FAILED="FAILED"; CANCELLED="CANCELLED"; BLOCKED="BLOCKED"
@dataclass
class Task:
    task_id: str; name: str; action: Callable[[], Any]; priority: int=0; dependencies: set[str]=field(default_factory=set); status: TaskStatus=TaskStatus.QUEUED

class TaskRuntime:
    def __init__(self, workers: int=4) -> None: self.executor=ThreadPoolExecutor(max_workers=max(1,workers)); self.tasks: dict[str,Task]={}; self.futures: dict[str,Future[Any]]={}; self.cancel_events: dict[str,CancelEvent]={}
    def submit(self, task: Task) -> Future[Any]:
        self.tasks[task.task_id]=task; task.status=TaskStatus.RUNNING
        future=self.executor.submit(self._run,task); self.futures[task.task_id]=future; return future
    def _run(self, task: Task) -> Any:
        try: result=task.action(); task.status=TaskStatus.SUCCEEDED; return result
        except Exception: task.status=TaskStatus.FAILED; raise
    def cancel(self, task_id: str) -> bool:
        task=self.tasks.get(task_id)
        if not task: return False
        task.status=TaskStatus.CANCELLED
        return self.futures.get(task_id, Future()).cancel()

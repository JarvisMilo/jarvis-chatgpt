from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any, Callable

@dataclass(frozen=True)
class Event:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[Event], None]]] = {}
        self._lock = RLock()
    def subscribe(self, name: str, handler: Callable[[Event], None]) -> None:
        with self._lock: self._handlers.setdefault(name, []).append(handler)
    def publish(self, event: Event) -> None:
        with self._lock: handlers = list(self._handlers.get(event.name, [])) + list(self._handlers.get("*", []))
        for handler in handlers: handler(event)

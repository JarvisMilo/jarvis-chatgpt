from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4


@dataclass
class ActionRecord:
    action_id: str
    tool: str
    arguments: dict[str, Any]
    result: Any
    reversible: bool
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    undo: Callable[[], Any] | None = None


class ActionJournal:
    def __init__(self) -> None:
        self.records: list[ActionRecord] = []

    def next_id(self) -> str:
        return uuid4().hex

    def record(self, record: ActionRecord) -> None:
        self.records.append(record)

    def last(self) -> ActionRecord | None:
        return self.records[-1] if self.records else None

    def undo_last(self) -> Any:
        for record in reversed(self.records):
            if record.reversible and record.undo is not None:
                return record.undo()
        raise RuntimeError("No reversible action available")

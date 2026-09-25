from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Memory:
    id: int
    kind: str
    content: str
    created_at: str
    updated_at: str


class MemoryRepository:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY,
                    kind TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )"""
            )
            db.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at)"
            )

    def save(self, kind: str, content: str) -> Memory:
        if not kind.strip() or not content.strip():
            raise ValueError("Memory kind and content cannot be empty")
        now = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.path) as db:
            cur = db.execute(
                "INSERT INTO memories(kind,content,created_at,updated_at) VALUES(?,?,?,?)",
                (kind.strip(), content, now, now),
            )
            return Memory(cur.lastrowid, kind.strip(), content, now, now)

    def get(self, memory_id: int) -> Memory | None:
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                "SELECT id,kind,content,created_at,updated_at FROM memories WHERE id=?",
                (memory_id,),
            ).fetchone()
        return Memory(*row) if row else None

    def list(self, limit: int = 100) -> list[Memory]:
        if limit < 1:
            return []
        with sqlite3.connect(self.path) as db:
            rows = db.execute(
                "SELECT id,kind,content,created_at,updated_at FROM memories ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [Memory(*row) for row in rows]

    def recent(self, limit: int = 10) -> list[Memory]:
        return self.list(limit)

    def update(self, memory_id: int, *, kind: str | None = None, content: str | None = None) -> Memory:
        current = self.get(memory_id)
        if current is None:
            raise KeyError(f"Memory not found: {memory_id}")
        new_kind = current.kind if kind is None else kind.strip()
        new_content = current.content if content is None else content
        if not new_kind or not new_content:
            raise ValueError("Memory kind and content cannot be empty")
        now = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.path) as db:
            db.execute(
                "UPDATE memories SET kind=?, content=?, updated_at=? WHERE id=?",
                (new_kind, new_content, now, memory_id),
            )
        return self.get(memory_id)  # type: ignore[return-value]

from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone

@dataclass
class Memory:
    id:int
    kind:str
    content:str
    created_at:str

class MemoryRepository:
    def __init__(self,path:Path):
        self.path=path
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, kind TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL)")
    def save(self,kind:str,content:str)->Memory:
        ts=datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.path) as db:
            cur=db.execute("INSERT INTO memories(kind,content,created_at) VALUES(?,?,?)",(kind,content,ts))
            return Memory(cur.lastrowid,kind,content,ts)
    def recent(self,limit:int=10)->list[Memory]:
        with sqlite3.connect(self.path) as db:
            rows=db.execute("SELECT id,kind,content,created_at FROM memories ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
        return [Memory(*r) for r in rows]

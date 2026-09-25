from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os, shutil

@dataclass(frozen=True)
class Application:
    name: str; executable: str|None=None; source: str="unknown"; arguments: str=""

def discover_applications() -> list[Application]:
    found: dict[str,Application]={}
    roots=[]
    for value in (os.environ.get("ProgramData"),os.environ.get("APPDATA"),os.environ.get("LOCALAPPDATA")):
        if value: roots.append(Path(value))
    for root in roots:
        for path in root.glob("Microsoft/Windows/Start Menu/Programs/**/*.lnk"):
            found.setdefault(path.stem.lower(),Application(path.stem,None,"start_menu"))
    for exe in ("python","python3","git","ollama","code","chrome","msedge"):
        hit=shutil.which(exe)
        if hit: found.setdefault(exe,Application(exe,hit,"path"))
    return sorted(found.values(), key=lambda a:a.name.lower())

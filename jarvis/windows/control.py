from __future__ import annotations
import os, subprocess
from pathlib import Path

class WindowsControl:
    """Minimal policy-ready control surface; never accepts arbitrary shell strings."""
    ALLOWED_PROTOCOLS={"https","http","mailto"}
    def open_path(self,path: str)->dict[str,object]:
        p=Path(path).expanduser().resolve()
        if not p.exists(): raise FileNotFoundError(str(p))
        os.startfile(str(p))
        return {"opened":str(p)}
    def launch_executable(self, executable: str, args: list[str]|None=None)->dict[str,object]:
        if not Path(executable).is_file(): raise FileNotFoundError(executable)
        subprocess.Popen([executable,*(args or [])], shell=False)
        return {"launched":executable}

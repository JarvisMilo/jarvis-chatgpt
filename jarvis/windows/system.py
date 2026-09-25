from __future__ import annotations
import os, platform, shutil

def snapshot()->dict[str,object]:
    return {"os":platform.platform(),"python":platform.python_version(),"cpu_count":os.cpu_count(),"disk_free_bytes":shutil.disk_usage(os.getcwd()).free}

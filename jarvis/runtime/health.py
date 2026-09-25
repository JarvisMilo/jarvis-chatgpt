from __future__ import annotations
import importlib.util, shutil
class HealthReport:
    def check(self,ollama_url,model,workspace):
        return {"python":True,"ollama_cli":bool(shutil.which("ollama")),"model":model,"workspace_exists":workspace.exists(),"playwright":bool(importlib.util.find_spec("playwright")),"pyqt6":bool(importlib.util.find_spec("PyQt6"))}

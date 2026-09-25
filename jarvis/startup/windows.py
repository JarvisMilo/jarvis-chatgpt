from __future__ import annotations
import os
class WindowsStartup:
    def __init__(self,name="JARVIS"): self.name=name
    @property
    def path(self): return os.path.join(os.environ.get("APPDATA",""),"Microsoft","Windows","Start Menu","Programs","Startup",f"{self.name}.cmd")
    def install(self,command):
        if os.name!="nt": return False
        os.makedirs(os.path.dirname(self.path),exist_ok=True)
        with open(self.path,"w",encoding="utf-8") as f: f.write("@echo off\n"+command+"\n")
        return True
    def uninstall(self):
        try: os.remove(self.path); return True
        except FileNotFoundError: return False

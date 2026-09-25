from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

class ToolError(RuntimeError): pass

@dataclass(frozen=True)
class Tool:
    name:str
    description:str
    handler:Callable[...,Any]
    risk:str="SAFE"
    reversible:bool=False
    requires_confirmation:bool=False

class ToolRegistry:
    def __init__(self): self._tools:dict[str,Tool]={}
    def register(self,tool:Tool)->None:
        if tool.name in self._tools: raise ToolError(f"Duplicate tool: {tool.name}")
        self._tools[tool.name]=tool
    def get(self,name:str)->Tool:
        try: return self._tools[name]
        except KeyError as e: raise ToolError(f"Unknown tool: {name}") from e
    def list(self)->list[Tool]: return list(self._tools.values())
    def execute(self,name:str,**kwargs)->dict:
        tool=self.get(name)
        if tool.requires_confirmation or tool.risk in {"DANGEROUS","EXTERNAL_SIDE_EFFECT"}:
            return {"success":False,"data":None,"error":"CONFIRMATION_REQUIRED","warnings":[],"artifacts":[]}
        try:
            return {"success":True,"data":tool.handler(**kwargs),"error":None,"warnings":[],"artifacts":[]}
        except Exception as e:
            return {"success":False,"data":None,"error":str(e),"warnings":[],"artifacts":[]}

def safe_ping()->str: return "pong"

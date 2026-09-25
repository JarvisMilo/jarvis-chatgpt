from __future__ import annotations
import json, urllib.error, urllib.request
from dataclasses import dataclass
from typing import Iterator

class LLMError(RuntimeError): pass

@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

class LLMProvider:
    def chat(self, messages:list[ChatMessage], *, stream:bool=True) -> Iterator[str]:
        raise NotImplementedError

class OllamaProvider(LLMProvider):
    def __init__(self, base_url:str, model:str, timeout:float=120):
        self.base_url=base_url.rstrip("/")
        self.model=model
        self.timeout=timeout

    def _request(self, path:str, payload:dict):
        data=json.dumps(payload).encode()
        req=urllib.request.Request(self.base_url+path,data=data,headers={"Content-Type":"application/json"},method="POST")
        try:
            return urllib.request.urlopen(req,timeout=self.timeout)
        except urllib.error.URLError as e:
            raise LLMError(f"Ollama unavailable: {e}") from e

    def chat(self,messages:list[ChatMessage],*,stream:bool=True)->Iterator[str]:
        payload={"model":self.model,"messages":[m.__dict__ for m in messages],"stream":stream}
        try:
            with self._request("/api/chat",payload) as response:
                for raw in response:
                    if not raw.strip(): continue
                    try: obj=json.loads(raw)
                    except json.JSONDecodeError as e: raise LLMError("Ollama returned invalid JSON") from e
                    if obj.get("error"): raise LLMError(str(obj["error"]))
                    chunk=obj.get("message",{}).get("content","")
                    if chunk: yield chunk
        except TimeoutError as e:
            raise LLMError("Ollama request timed out") from e

    def health(self)->bool:
        req=urllib.request.Request(self.base_url+"/api/tags",method="GET")
        try:
            with urllib.request.urlopen(req,timeout=5): return True
        except (urllib.error.URLError,TimeoutError): return False

    def models(self)->list[str]:
        req=urllib.request.Request(self.base_url+"/api/tags",method="GET")
        try:
            with urllib.request.urlopen(req,timeout=5) as r:
                data=json.load(r)
            return [m.get("name","") for m in data.get("models",[]) if m.get("name")]
        except (urllib.error.URLError,TimeoutError,json.JSONDecodeError) as e:
            raise LLMError(f"Could not read Ollama models: {e}") from e

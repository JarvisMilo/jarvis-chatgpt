from __future__ import annotations
from dataclasses import dataclass
@dataclass
class RecoveryPolicy: max_attempts:int=2; backoff_seconds:float=.25
class RecoveryEngine:
    def __init__(self,policy=None): self.policy=policy or RecoveryPolicy()
    def run(self,operation,verify,alternatives=()):
        attempts=0; errors=[]
        for strategy in (operation,*alternatives):
            if attempts>=self.policy.max_attempts: break
            attempts+=1
            try:
                result=strategy()
                if verify(result): return {"success":True,"attempts":attempts,"result":result}
            except Exception as exc: errors.append(str(exc))
        return {"success":False,"attempts":attempts,"errors":errors}

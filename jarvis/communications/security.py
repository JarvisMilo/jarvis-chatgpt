from __future__ import annotations
class ExternalSendGate:
    def authorize(self,destination,content,confirmed=False):
        if not confirmed: return {"allowed":False,"reason":"EXPLICIT_CONFIRMATION_REQUIRED"}
        if not destination or not content: return {"allowed":False,"reason":"DESTINATION_AND_CONTENT_REQUIRED"}
        return {"allowed":True,"reason":"CONFIRMED"}

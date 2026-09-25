from __future__ import annotations
class ClipboardIntel:
    def classify(self,text):
        text=text or ""
        if not text: return "empty"
        if "@" in text and " " not in text: return "email-like"
        if text.lstrip().startswith(("http://","https://")): return "url"
        return "text"

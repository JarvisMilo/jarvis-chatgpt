from __future__ import annotations
class LanguageDetector:
    def detect(self,text):
        t=(text or "").lower()
        if any(x in t for x in (" el "," la "," que "," para "," una ")): return "es"
        if any(x in t for x in (" the "," and "," what "," with ")): return "en"
        return "unknown"

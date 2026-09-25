from __future__ import annotations
class InstantAcknowledgment:
    def phrase(self,task,language="es"):
        if language=="es": return f"Entendido. Inicio {task}." if task else "Entendido. Lo proceso ahora."
        return f"Understood. Starting {task}." if task else "Understood. Processing it now."

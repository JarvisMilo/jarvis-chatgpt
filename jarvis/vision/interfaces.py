from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class Observation:
    text: str=""; elements: tuple[dict, ...]=(); source: str="unknown"
class VisionEngine(ABC):
    @abstractmethod
    def observe(self, image: bytes)->Observation: ...

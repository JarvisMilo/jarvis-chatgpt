from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(level: str = "INFO", log_file: Path | None = None) -> logging.Logger:
    logger = logging.getLogger("jarvis")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logger.addHandler(stream)
    if log_file and not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        logger.addHandler(handler)
    return logger

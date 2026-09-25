import logging
from pathlib import Path

def configure_logging(level: str="INFO", log_file: Path|None=None) -> logging.Logger:
    logger=logging.getLogger("jarvis")
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging,level.upper(),logging.INFO))
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    sh=logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    if log_file:
        log_file.parent.mkdir(parents=True,exist_ok=True)
        fh=logging.FileHandler(log_file,encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger

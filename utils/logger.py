"""Small file logger used for unexpected application errors."""

import logging

from config import PROJECT_ROOT


def get_logger() -> logging.Logger:
    """Return the application logger without adding duplicate handlers."""
    logger = logging.getLogger("presenza")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "presenza.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    return logger

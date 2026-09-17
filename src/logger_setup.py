"""
Centralized logging configuration.

NEW module. Nothing in the original project writes logs to disk — train.py
only prints to stdout, so training runs, accuracy, and errors aren't
recorded anywhere. This gives every module a consistent logger that writes
to logs/nids.log as well as the console.

Usage (optional — see docs/SETUP_AND_RUN_GUIDE.pdf for exactly where to
add these two lines in your existing files):

    from src.logger_setup import get_logger
    logger = get_logger(__name__)
    logger.info("Model trained successfully")
"""
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "nids.log"

_CONFIGURED = False


def _configure_root():
    global _CONFIGURED
    if _CONFIGURED:
        return
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root = logging.getLogger("nids")
    root.setLevel(logging.INFO)
    root.addHandler(file_handler)
    root.addHandler(console_handler)
    _CONFIGURED = True


def get_logger(name="nids"):
    _configure_root()
    return logging.getLogger(f"nids.{name}" if name != "nids" else "nids")

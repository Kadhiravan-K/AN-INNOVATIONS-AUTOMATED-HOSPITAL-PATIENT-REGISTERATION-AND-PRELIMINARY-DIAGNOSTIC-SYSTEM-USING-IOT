# ─────────────────────────────────────────────────────────────────
# utils/logger.py — Centralized logging for the application
# ─────────────────────────────────────────────────────────────────

import logging
import sys
from config import LOG_FILE, LOG_LEVEL


def get_logger(name="hospital_kiosk"):
    """
    Returns a configured logger instance.
    Logs to both console and file.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)-7s]  %(name)-20s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        logger.warning("Could not create log file. Logging to console only.")

    return logger

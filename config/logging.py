"""
Logging configuration for Project Chitti - Cognitive Edge Sentry.

Provides JSON-formatted structured logging for machine-parseable evidence.
All logs are written to ~/chitti/data/logs/ per the Directory Lock directive.
"""

import json
import logging
from pathlib import Path
from typing import Optional

from config.settings import LOG_DIR, LOG_LEVEL, LOG_FORMAT_JSON


class JSONFormatter(logging.Formatter):
    """Format log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        """Serialize a log record to JSON."""
        entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        extra = getattr(record, "extra", None)
        if extra:
            entry["extra"] = extra
        return json.dumps(entry)


def setup_logging(module_name: Optional[str] = None) -> None:
    """
    Configure logging handlers for the application.

    Args:
        module_name: If provided, also writes to a dedicated
                     log file at ~/chitti/data/logs/{module_name}.log.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    if root_logger.handlers:
        return  # Already configured

    root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    formatter: logging.Formatter
    if LOG_FORMAT_JSON:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    if module_name:
        log_file = LOG_DIR / f"{module_name}.log"
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

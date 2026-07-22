"""Structured logging service using structlog."""

import logging
import sys

import structlog

from config import LOG_LEVEL, LOGS_DIR


def setup_logging() -> structlog.stdlib.BoundLogger:
    LOGS_DIR.mkdir(exist_ok=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(LOGS_DIR / "app.log"),
        ],
    )

    return structlog.get_logger()


logger = setup_logging()

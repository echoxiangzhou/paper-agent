"""
Logging Configuration

Structured logging setup for the application.
"""

import logging
import logging.config
import sys
from typing import Any, Dict

from app.core.config import settings


def setup_logging() -> None:
    """Configure application logging."""
    
    # Define log format
    if settings.LOG_FORMAT == "json":
        log_format = {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    else:
        log_format = {
            "format": "%(asctime)s | %(levelname)8s | %(name)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    
    # Logging configuration
    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": log_format,
            "access": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "": {  # root logger
                "level": settings.LOG_LEVEL,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["access"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "handlers": ["default"],
                "propagate": False,
            },
            "celery": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
        },
    }
    
    # Apply configuration
    logging.config.dictConfig(config)
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
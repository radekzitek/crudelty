# backend/app/core/logger.py
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import sys
from pathlib import Path
from .config import get_settings
from .. import __version__

def setup_logger(name: str) -> logging.Logger:
    """Configure application logging"""
    settings = get_settings()

    name = name+" v"+__version__
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # Clear existing handlers   
    logger.handlers.clear()
    
    # Create formatters and handlers
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Console handler
    if settings.LOG_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(settings.LOG_LEVEL)
        logger.addHandler(console_handler)
    
    # File handler if LOG_FILE is specified
    if settings.LOG_FILE:
        log_file = Path(settings.LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Time-based rotation: rotate at "midnight", "S", "M", "H", "D", "W0-W6"
        time_handler = TimedRotatingFileHandler(
            settings.LOG_FILE,
            when=settings.LOG_ROTATE_WHEN,
            interval=settings.LOG_ROTATE_INTERVAL,
            backupCount=settings.LOG_ROTATE_BACKUPS,
            encoding='utf-8'
        )
        time_handler.setFormatter(formatter)
        time_handler.setLevel(settings.LOG_LEVEL)
        logger.addHandler(time_handler)
    
    logger.debug(f"Logger setup complete. Log level {settings.LOG_LEVEL}")
    if settings.LOG_FILE:
        logger.debug(f"Log file: {settings.LOG_FILE}")
    else:
        logger.debug("No log file specified")
    if settings.LOG_CONSOLE:
        logger.debug("Console logging enabled")
    else:
        logger.debug("Console logging disabled")

    return logger

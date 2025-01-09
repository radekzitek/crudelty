# backend/app/core/logger.py
import logging
from logging.handlers import RotatingFileHandler
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
from .config import get_settings
from .redis_logger import redis_logger
import asyncio

settings = get_settings()

class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        # Base log record
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add request_id if available
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
            
        # Add error details if available
        if record.exc_info:
            log_obj["error"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
            
        # Add extra fields
        for key, value in record.__dict__.items():
            if key.startswith("_") or key in ["name", "msg", "args", "exc_info", "exc_text"]:
                continue
            log_obj[key] = value
        
        # Schedule Redis logging asynchronously
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(redis_logger.log(
                    level=record.levelname,
                    message=record.getMessage(),
                    **log_obj
                ))
        except Exception:
            # If Redis logging fails, continue with file logging
            pass
            
        return json.dumps(log_obj)

def setup_logger(name: str) -> logging.Logger:
    """Setup and return a logger instance"""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = CustomJsonFormatter()
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        filename="logs/error.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.DEBUG)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

import logging
import os
from .config import settings

def setup_logging():
    """Set up logging configuration for both console and file output."""
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
    
    # Create formatter
    log_formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # File handler
    file_handler = logging.FileHandler(settings.LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(log_formatter)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add our handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 
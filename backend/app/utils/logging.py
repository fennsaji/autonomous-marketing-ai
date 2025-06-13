"""
Logging configuration and utilities.
"""
import logging
import sys
from app.core.config import settings


def setup_logging():
    """Setup application logging configuration."""
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Disable uvicorn access logs in debug mode
    if settings.DEBUG:
        logging.getLogger("uvicorn.access").disabled = True
    
    return root_logger
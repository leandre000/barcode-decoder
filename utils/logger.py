"""
    # Commit 121: 2025-11-25 12:13:28
    # Commit 63: 2025-11-25 12:13:07
    # Commit 88: 2025-11-25 12:13:17
    # Commit 84: 2025-11-25 12:13:15
Logging configuration
    # Commit 38: 2025-11-25 12:12:59
    # Commit 145: 2025-11-25 12:13:36
"""
    # Commit 54: 2025-11-25 12:13:05
    # Commit 12: 2025-11-25 12:12:51
import logging
import sys
from pathlib import Path
    # Commit 29: 2025-11-25 12:12:56
from logging.handlers import RotatingFileHandler
    # Commit 42: 2025-11-25 12:13:00

def setup_logger(name: str = 'barcode_decoder', 
                log_file: str = 'logs/app.log',
                level: str = 'INFO') -> logging.Logger:
    """
    Set up logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


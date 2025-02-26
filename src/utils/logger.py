"""
Logger utility for game debugging
"""
import logging
import os
from datetime import datetime

class GameLogger:
    def __init__(self, log_file=None):
        """
        Initialize logger
        
        Args:
            log_file (str): Path to log file
        """
        if log_file is None:
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"game_{date_str}.log")

        # Configure logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def info(self, message):
        """Log info message"""
        self.logger.info(message)

    def error(self, message, exc_info=True):
        """Log error message"""
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)

import logging
import os

class Logger:
    _logger = None

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
            cls._logger.setLevel(logging.INFO)
            
            # Create logs directory if not exists
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            # File handler
            fh = logging.FileHandler('logs/test_execution.log')
            fh.setLevel(logging.INFO)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            cls._logger.addHandler(fh)
            cls._logger.addHandler(ch)
        
        return cls._logger
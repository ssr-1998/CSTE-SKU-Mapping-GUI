import logging
import os
from datetime import datetime

def setup_logger(name='app_logger', level=logging.INFO):

    # Create Logs Directory if Not Exists
    os.makedirs('logs', exist_ok=True)

    # Timestamp for Filename, e.g. app_2025-08-07_13-00-00.log
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"app_{timestamp}.log"
    log_path = os.path.join('logs', log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        fh = logging.FileHandler(log_path)
        fh.setLevel(level)

        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

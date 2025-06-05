import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

date_str = datetime.now().strftime("%Y-%m-%d")

ERROR_LOG_FILE = os.path.join(LOG_DIR, f"errors_{date_str}.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

error_file_handler = logging.FileHandler(ERROR_LOG_FILE, mode="a", encoding="utf-8")
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(error_file_handler)
    logger.addHandler(console_handler)
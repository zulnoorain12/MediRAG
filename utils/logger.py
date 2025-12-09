from loguru import logger
import sys
from datetime import datetime

# Remove default logger
logger.remove()

# Log to file + console
log_file = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
logger.add(log_file, rotation="500 MB", retention="10 days", level="INFO")
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

# Create logs folder if not exists
import os
if not os.path.exists("logs"):
    os.makedirs("logs")

logger.info("MediRAG Logger initialized")
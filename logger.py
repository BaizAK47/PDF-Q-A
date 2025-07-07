# logger.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),     # Save to file
        logging.StreamHandler()             # Also show in terminal
    ]
)

logger = logging.getLogger(__name__)

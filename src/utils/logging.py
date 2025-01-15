import logging
import os
import sys
from datetime import datetime


def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_filename = f"logs/carbon_calculator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_filename),
        ],
    )

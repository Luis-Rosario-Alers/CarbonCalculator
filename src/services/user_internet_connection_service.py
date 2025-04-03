import logging

import requests

logger = logging.getLogger("services")


def user_internet_connection_check():
    logger.info("Testing internet connection")
    try:
        response = requests.get("https://www.google.com/", timeout=5)
        if response.status_code == 200:
            logger.info("Internet connection established.")
            return True
    except requests.exceptions.RequestException as e:
        logger.error(f"an error occurred testing internet connection: {e}")
        logger.info("Program will now proceed in offline mode.")
        logger.info("Note: Some features may not be available.")
        return False

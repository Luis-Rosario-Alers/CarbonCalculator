import logging
import os

from dotenv import load_dotenv

from utils.logging import setup_logging

setup_logging()

logger = logging.getLogger("utilities")

load_dotenv(dotenv_path="src/utils/EXAMPLE_ENV.env")


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
IP_API_TOKEN = os.getenv("IP_API_TOKEN")

WEATHER_API_KEY_PLACEHOLDER = "your_weather_api_key_here"  # nosec
IP_API_TOKEN_PLACEHOLDER = "your_ip_api_key_here"  # nosec

# Check for missing or placeholder values
if (
    not IP_API_TOKEN
    or IP_API_TOKEN.strip() == ""
    or IP_API_TOKEN == IP_API_TOKEN_PLACEHOLDER
):
    logger.error("IP API token not found or is a placeholder")
    IP_API_TOKEN = None  # Treat as missing
else:
    logger.info("IP API token found")

if (
    not WEATHER_API_KEY
    or WEATHER_API_KEY.strip() == ""
    or WEATHER_API_KEY == WEATHER_API_KEY_PLACEHOLDER
):
    logger.error("Weather API key not found or is a placeholder")
    WEATHER_API_KEY = None  # Treat as missing
else:
    logger.info("Weather API key found")

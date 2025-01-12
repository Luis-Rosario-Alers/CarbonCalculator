import asyncio
import logging.config
import os

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

import data.database as db
from services.user_internet_connection_service import test_user_internet_connection
from services.user_location_service import UserLocationService
from services.weather_service import WeatherService
from ui.main_window import MainWindow
from utils.config import IP_API_TOKEN, WEATHER_API_KEY
from utils.logging import setup_logging

setup_logging()

logger = logging.getLogger("main")


user_local_temps = None


async def start():
    global user_local_temps
    """
    Initialize the databases and retrieve user location and weather data.

    This function initializes the databases if they do not exist, retrieves the user's
    location using the UserLocationService, and then fetches the weather data for the
    user's location using the WeatherService.

    """
    logger.info("Initializing databases")
    if not os.path.exists("databases"):
        await db.database_initialization()
    logger.info("Databases initialized")
    internet_connection_process = await test_user_internet_connection()
    if (
        WEATHER_API_KEY is None
        or IP_API_TOKEN is None
        or internet_connection_process is False
    ):
        logger.warning("Continuing program without local temperatures")
        user_local_temps = None
        return internet_connection_process
    else:
        user_location_service = UserLocationService(IP_API_TOKEN)
        weather_service = WeatherService(WEATHER_API_KEY)
        user_coords = await user_location_service.get_user_location()

        if user_coords is None:
            logger.error("Failed to retrieve user coordinates")
            logger.warning("Continuing program without local temperatures")
            user_local_temps = None
        else:
            user_local_temps = await weather_service.get_weather(
                user_coords[0], user_coords[1]
            )

        return internet_connection_process  # return internet_connection_process


def run_main_window(internet_connection_status_passed):
    """
    Run the event loop for the main window.

    This function creates the application instance, sets up the Qt event loop
    integrating it with the asyncio loop, and runs the main window of the application.
    """
    logger.info("Running main window")

    # Create application instance
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow(internet_connection_status_passed)
    main_window.show()

    with loop:
        loop.run_forever()


def main():
    """
    Main entry point for the application.

    This function starts the application by initializing the event loop, running the
    startup tasks, and then running the main window.
    """
    logger.info("Starting application")
    loop = asyncio.get_event_loop()
    internet_connection_status = loop.run_until_complete(start())
    run_main_window(internet_connection_status)


if __name__ == "__main__":
    main()


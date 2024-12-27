import asyncio
import logging
import logging.config
import os

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

import data.database as db
from ui.main_window import MainWindow
from utils.logging import setup_logging

setup_logging()

logger = logging.getLogger("main")


async def start():
    # * this is used to initialize the databases
    logger.info("Initializing databases")
    if not os.path.exists("databases"):
        await db.database_initialization()
    logger.info("Databases initialized")


def run_main_window():
    # * this is used to run the event loop for the main window
    logger.info("Running main window")

    # Create application instance
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
        loop.run_forever()


def main():
    logger.info("Starting application")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    run_main_window()


if __name__ == "__main__":
    main()

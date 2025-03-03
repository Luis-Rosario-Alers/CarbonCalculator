import asyncio
import logging.config
import os
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from src.ui.main_window import MainWindowWidget


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


setup_logging()
logger = logging.getLogger("main")


def main():
    """
    Main entry point for the application.

    This function starts the application by initializing the event loop, running the
    startup tasks, and then running the main window.
    """
    logger.info("Starting application")
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindowWidget()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()

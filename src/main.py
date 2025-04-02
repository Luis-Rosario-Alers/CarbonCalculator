import logging.config
import os
import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindowWidget


def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_filename = (
        f"logs/carbon_calculator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

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

    This function starts the application by initializing QApplication
    and then running the main window.
    """
    logger.info("Starting application")
    app = QApplication([])

    # Set a reasonable number of threads in the global thread pool
    # Default is typically number of cores, but we can adjust if needed
    # QThreadPool.globalInstance().setMaxThreadCount(4)

    # Create and show the main window
    MainWindowWidget()

    # Run the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

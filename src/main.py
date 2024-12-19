import asyncio
import os
import sys

from PyQt5.QtWidgets import QApplication

import data.database as db
from ui.main_window import MainWindow


async def start():
    if not os.path.exists("databases"):
        await db.database_initialization()


def run_main_window():
    # * this is used to run the event loop for the main window

    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    run_main_window()


if __name__ == "__main__":
    main()

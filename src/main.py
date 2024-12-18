import asyncio
import os

from PyQt5.QtWidgets import QApplication

import data.database as db
from ui.main_window import MainWindow


async def Start():
    if not os.path.exists("databases"):
        await db.database_initialization()
    RunMainWindow()


def RunMainWindow():
    #  * This function is used to run the main window of the application

    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()


def main():
    asyncio.run(Start())

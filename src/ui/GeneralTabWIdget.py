import logging
import os

import aiosqlite
from PySide6.QtCore import QObject, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QTableView, QWidget

from data.database import databases_folder
from src.ui.generated_python_ui.ui_generalTabWidget import Ui_GeneralWidget
from src.utils.gui_utilities import connect_async

logger = logging.getLogger("ui")


class GeneralTabController(QObject):
    def __init__(self, model, view, application_controller):
        super().__init__()
        self.model = model
        self.view = view
        self.application_controller = application_controller
        self.__connect_signals()

    def __connect_signals(self):
        connect_async(
            self.model.database_model,
            "databases_initialized",
            self.handle_database_widget_changed,
        )
        connect_async(
            self.application_controller,
            "application_closed",
            self.handle_application_close,
        )

    async def handle_database_widget_changed(self):
        await self.model.load_database_table_content()
        await self.view.load_database_table()

    async def handle_application_close(self):
        logger.debug("GeneralTabWidget: closing database connection")
        await self.view.close_database_on_application_close()


class GeneralTabModel:
    def __init__(self, database_model):
        self.database_model = database_model

    async def load_database_table_content(self):
        # Get database path
        db_path = os.path.join(databases_folder, "emissions.db")

        # Connect to database
        async with aiosqlite.connect(db_path) as conn:
            # Enable row factory to get column names
            conn.row_factory = aiosqlite.Row

            # Execute query to get all data
            async with conn.execute(
                "SELECT * FROM emissions ORDER BY timestamp DESC"
            ) as cursor:
                rows = await cursor.fetchall()
                # Get column names from cursor description
                columns = [
                    description[0] for description in cursor.description
                ]
                return rows, columns


class GeneralTabView(QWidget, Ui_GeneralWidget):
    database_widget_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.database_loaded = False

    async def load_database_table(self):
        if not self.database_loaded:
            logger.info("loading database table")
            # Set up database connection
            self.db_connection = QSqlDatabase.addDatabase("QSQLITE")
            db_path = os.path.join(databases_folder, "emissions.db")
            self.db_connection.setDatabaseName(db_path)

            if not self.db_connection.open():
                logger.error(
                    f"Failed to open database: {self.db_connection.lastError().text()}"
                )
                return

            # Create and configure the model
            self.sql_widget_model = QSqlTableModel(self, self.db_connection)
            self.sql_widget_model.setTable("emissions")

            if hasattr(self, "sqlTableView"):
                self.sqlTableView.setEditTriggers(QTableView.NoEditTriggers)
                self.sql_widget_model.select()
                self.sqlTableView.setModel(self.sql_widget_model)
                self.sqlTableView.resizeColumnsToContents()
            else:
                logger.error("sqlTableView not found in UI")
            self.database_loaded = True
        else:
            logger.debug("Database already loaded, skipping")

    async def close_database_on_application_close(self):
        logger.info("closing database connection.")
        await self.db_connection.close()


class GeneralTabWidget(QWidget):
    def __init__(self, database_model, application_controller):
        super().__init__()
        self.database_model = database_model
        self.application_controller = application_controller
        self.model = GeneralTabModel(self.database_model)
        self.view = GeneralTabView()
        self.controller = GeneralTabController(
            self.model, self.view, self.application_controller
        )

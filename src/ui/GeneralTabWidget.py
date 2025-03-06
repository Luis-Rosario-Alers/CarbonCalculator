import logging
import os

from PySide6.QtCore import QObject, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QTableView, QWidget

from data.database import databases_folder
from src.ui.generated_python_ui.ui_generalTabWidget import Ui_GeneralWidget
from src.utils.gui_utilities import connect_threaded

logger = logging.getLogger("ui")


class GeneralTabController(QObject):
    def __init__(self, model, view, application_controller):
        super().__init__()
        self.model = model
        self.view = view
        self.application_controller = application_controller
        self.__connect_signals()

    def __connect_signals(self):
        connect_threaded(
            self.model.database_model,
            "databases_initialized",
            self.handle_database_widget_changed,
        )
        connect_threaded(
            self.application_controller,
            "application_closed",
            self.handle_application_close,
        )
        connect_threaded(
            self.view.calculateContainerPushButton,
            "clicked",
            self.handle_calculate_button_clicked,
        )

    def handle_database_widget_changed(self):
        self.model.load_database_table_content()
        self.view.load_database_table()

    def handle_calculate_button_clicked(self):
        logger.debug("GeneralTabWidget: calculate button clicked")

    def handle_application_close(self):
        logger.debug("GeneralTabWidget: closing database connection")
        self.view.close_database_on_application_close()


class GeneralTabModel:
    def __init__(self, database_model):
        self.database_model = database_model

    def load_database_table_content(self):
        pass


class GeneralTabView(QWidget, Ui_GeneralWidget):
    database_widget_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.database_loaded = False
        self.db_connection = None
        self.sql_widget_model = None

    def load_database_table(self):
        if not self.database_loaded:
            logger.info("Loading database table")
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

            # Check if select() succeeded
            if not self.sql_widget_model.select():
                logger.error(
                    f"Failed to select data: {self.sql_widget_model.lastError().text()}"
                )
                return

            if hasattr(self, "sqlTableView"):
                self.sqlTableView.setEditTriggers(QTableView.NoEditTriggers)
                # Explicitly set the model after select() has completed
                self.sqlTableView.setModel(self.sql_widget_model)

                # Make sure columns are visible
                self.sqlTableView.horizontalHeader().setVisible(True)
                self.sqlTableView.resizeColumnsToContents()

                # Check row count for debugging
                row_count = self.sql_widget_model.rowCount()
                logger.info(f"Loaded {row_count} rows from emissions table")

            else:
                logger.error("sqlTableView not found in UI")
            self.database_loaded = True
        else:
            logger.debug("Database already loaded, skipping")

    def close_database_on_application_close(self):
        logger.info("closing database connection.")
        if self.db_connection and self.db_connection.isOpen():
            self.db_connection.close()


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

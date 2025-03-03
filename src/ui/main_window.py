import logging
import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from src.data.database import databasesModel
from ui.generated_python_ui.ui_main_window import Ui_MainWindow

logger = logging.getLogger("ui")


# Controller: controls data for the MainWindow
class MainWindowController(QObject):
    initialization = Signal()

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.initialization.emit()
        logger.info("emitted initialization signal")

    # __connect_signals(self):


# Model: The app model handles APPLICATION WIDE STATE.
class AppModel(QObject):
    def __init__(self):
        super().__init__()
        pass


# View: controls the UI for the Main Window
class MainWindowView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        logger.info("Showing Main Window")


# Widget: Ties the View, Controller, and Model together
class MainWindowWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create model and controller
        self.model = AppModel()
        self.view = MainWindowView()
        self.controller = MainWindowController(self.model, self.view)
        self.databasesModel = databasesModel(self.controller)

    """
    def setup_tab_widgets(self):
        # Replace mainBody placeholder with stacked widget
        self.stacked_widget = QStackedWidget()
        self.horizontalLayout.replaceWidget(self.mainBody, self.stacked_widget)

        # Create tab widgets and add to stack
        self.general_tab = GeneralTabWidget(self.model, self.controller)
        self.visualization_tab = VisualizationTabWidget(self.model, self.controller)
        self.ai_chat_tab = AIChatTabWidget(self.model, self.controller)

        self.stacked_widget.addWidget(self.general_tab)
        self.stacked_widget.addWidget(self.visualization_tab)
        self.stacked_widget.addWidget(self.ai_chat_tab)
    """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindowWidget()
    sys.exit(app.exec())

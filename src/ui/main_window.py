import logging
import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from core.emissions_calculator import calculationModel
from src.data.database import databasesModel
from ui.GeneralTabWidget import GeneralTabWidget
from ui.generated_python_ui.ui_main_window import Ui_MainWindow
from utils.gui_utilities import connect_threaded

logger = logging.getLogger("ui")


# Controller: controls data for the MainWindow
class MainWindowController(QObject):
    initialization = Signal()
    application_closed = Signal()

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.__connect_signals()

    def __connect_signals(self):
        # Application wide signals
        connect_threaded(
            self.view, "main_window_closed", self.handle_main_window_closed
        )

        # calculation model signals
        self.model.calculation_model.calculation_result.connect(
            self.model.databases_model.log_calculation
        )

    def send_initialization_signal(self):
        self.initialization.emit()  # this starts the initialization sequence

    def handle_main_window_closed(self):
        logger.debug("emitting application closed signal")
        self.application_closed.emit()


# Model: The app model handles APPLICATION WIDE STATE.
class AppModel(QObject):
    def __init__(self):
        super().__init__()
        self.databases_model = databasesModel()
        self.calculation_model = calculationModel()

    def setup_models(self, main_window_controller):
        self.databases_model.set_controller(main_window_controller)
        self.calculation_model.set_controller(main_window_controller)


# View: controls the UI for the Main Window
class MainWindowView(QMainWindow, Ui_MainWindow):
    main_window_closed = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setup_tabs(self, model, controller):
        general_tab = GeneralTabWidget(model, controller)

        self.stackedWidget.addWidget(general_tab.view)
        self.stackedWidget.setCurrentWidget(general_tab.view)

        self.menuGeneral.addAction("General").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(general_tab.view)
        )

    def closeEvent(self, event):
        self.main_window_closed.emit()
        event.accept()
        logger.info("Main window closed")


# Widget: Ties the View, Controller, and Model together
class MainWindowWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create model and controller
        self.model = AppModel()
        self.view = MainWindowView()
        self.controller = MainWindowController(self.model, self.view)
        self.model.setup_models(
            self.controller
        )  # setups up application wide models
        self.view.setup_tabs(
            self.model, self.controller
        )  # setups up all tabs for application

        self.controller.send_initialization_signal()  # send signal to initialize all models
        self.view.show()

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

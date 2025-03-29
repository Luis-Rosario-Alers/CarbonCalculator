import logging
import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from data.settings_model import SettingsModel
from src.core.emissions_calculator import calculationModel
from src.data.database_model import databasesModel
from src.ui.GeneralTabWidget import GeneralTabWidget
from src.ui.generated_python_ui.ui_main_window import Ui_MainWindow
from src.ui.VisualizationTabWidget import VisualizationTabWidget
from ui.FeedbackTabWidget import FeedbackTabWidget
from ui.HelpTabWidget import HelpTabWidget

logger = logging.getLogger("ui")


# Controller: controls data for the MainWindow
class MainWindowController(QObject):
    initialization = Signal()
    application_closed = Signal()
    tab_changed = Signal(int)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

    def connect_signals(self):
        logger.debug(
            "Main Window Controller: Connecting signals in MainWindowController"
        )
        # Application wide signals
        self.view.main_window_closed.connect(self.handle_main_window_closed)
        self.view.stackedWidget.currentChanged.connect(self.handle_tab_changed)

        # calculation model signals
        self.model.calculation_model.calculation_result.connect(
            self.model.databases_model.log_transaction
        )

    def send_initialization_signal(self):
        logger.debug("Main Window Controller: emitting initialization signal")
        self.initialization.emit()  # this starts the initialization sequence

    def handle_main_window_closed(self):
        logger.debug(
            "Main Window Controller: emitting application closed signal"
        )
        self.application_closed.emit()

    def handle_tab_changed(self, index):
        logger.debug(f"Tab changed to index {index}")
        self.tab_changed.emit(index)


# Model: The app model handles APPLICATION WIDE STATE.
class AppModel(QObject):
    def __init__(self):
        super().__init__()
        self.databases_model = databasesModel()
        self.calculation_model = calculationModel()
        self.settings_model = SettingsModel()

    def setup_models(self, main_window_controller):
        logger.debug("Main Window Model: Setting up models in AppModel")
        self.databases_model.set_controller(main_window_controller)
        self.calculation_model.set_controller(main_window_controller)
        self.settings_model.set_controller(main_window_controller)


# View: controls the UI for the Main Window
class MainWindowView(QMainWindow, Ui_MainWindow):
    main_window_closed = Signal()

    def __init__(self):
        super().__init__()
        self.FeedbackTabWidget = None
        self.HelpTabWidget = None
        self.GeneralTabWidget = None
        self.VisualizationTabWidget = None
        self.setupUi(self)

    def setup_tabs(self, model, controller):
        logger.debug("Main Window View: Setting up tabs in MainWindowView")
        self.GeneralTabWidget = GeneralTabWidget(model, controller)
        self.VisualizationTabWidget = VisualizationTabWidget(model, controller)
        self.HelpTabWidget = HelpTabWidget(controller, model)
        self.FeedbackTabWidget = FeedbackTabWidget(controller, model)

        self.stackedWidget.insertWidget(0, self.GeneralTabWidget.view)
        self.stackedWidget.insertWidget(1, self.VisualizationTabWidget.view)
        self.stackedWidget.insertWidget(2, QWidget())  # TODO: AI CHAT
        self.stackedWidget.insertWidget(3, self.HelpTabWidget.view)
        self.stackedWidget.insertWidget(4, self.FeedbackTabWidget.view)

        # set default to the general widget
        self.stackedWidget.setCurrentWidget(self.GeneralTabWidget.view)

        self.menuGeneral.addAction("General").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(
                self.GeneralTabWidget.view
            )
        )
        self.menuVisualization.addAction("Visualization").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(
                self.VisualizationTabWidget.view
            )
        )
        self.menuAI_chat.addAction("AI Chat").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(QWidget())
        )
        self.menuHelp.addAction("Help").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(
                self.HelpTabWidget.view
            )
        )
        self.menuFeedback.addAction("Feedback").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(
                self.FeedbackTabWidget.view
            )
        )

    def closeEvent(self, event):
        self.main_window_closed.emit()
        event.accept()
        logger.info("Main Window View: Closing...")


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
        self.controller.connect_signals()
        self.controller.send_initialization_signal()  # send signal to initialize all models
        self.view.show()

    """
    def setup_tab_widgets(self):
        # Replace mainBody placeholder with stacked widget
        self.stacked_widget = QStackedWidget()
        self.horizontalLayout.replaceWidget(self.mainBody, self.stacked_widget)

        # Create tab widgets and add to stack
        self.GeneralTabWidget = GeneralTabWidget(self.model, self.controller)
        self.VisualizationTabWidget = VisualizationTabWidget(self.model, self.controller)
        self.ai_chat_tab = AIChatTabWidget(self.model, self.controller)

        self.stacked_widget.addWidget(self.GeneralTabWidget)
        self.stacked_widget.addWidget(self.VisualizationTabWidget)
        self.stacked_widget.addWidget(self.ai_chat_tab)
    """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindowWidget()
    sys.exit(app.exec())

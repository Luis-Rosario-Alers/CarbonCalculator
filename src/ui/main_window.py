import logging
import os
import sys

from PySide6.QtCore import QObject, QTranslator, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from core.emissions_calculator import calculationModel
from data.database_model import application_path, databasesModel
from data.export_manager import ExportManager
from data.import_manager import ImportManager
from data.settings_model import SettingsModel
from ui.FeedbackTabWidget import FeedbackTabWidget
from ui.GeneralTabWidget import GeneralTabWidget
from ui.generated_python_ui.ui_main_window import Ui_MainWindow
from ui.HelpTabWidget import HelpTabWidget
from ui.VisualizationTabWidget import VisualizationTabWidget

logger = logging.getLogger("ui")


# Controller: controls data for the MainWindow
class MainWindowController(QObject):
    initialization = Signal()
    application_closed = Signal()
    tab_changed = Signal(int)
    theme_changed = Signal(bool)  # True if light mode, False if dark mode
    progress_updated = Signal(int, str)
    progress_complete = Signal()
    language_changed = Signal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

    def connect_signals(self):
        self.update_progress(70, "Connecting Signals")
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
        self.model.settings_model.theme_changed.connect(self.handle_theme_changed)

    # Yes, I know it's not the BEST solution, but we will get to it at some point.
    def update_progress(self, percentage, message):
        """
        Updates General Tab View progress bar
        :param percentage: percentage of progress
        :param message: message to display on progress bar.
        :return: Nothing
        """
        logger.debug(f"Progress update: {percentage}% - {message}")
        self.progress_updated.emit(percentage, message)
        if percentage >= 100:
            self.progress_complete.emit()

    def send_initialization_signal(self):
        logger.debug("Main Window Controller: emitting initialization signal")
        self.initialization.emit()  # this starts the initialization sequence

    def handle_main_window_closed(self):
        logger.debug("Main Window Controller: emitting application closed signal")
        self.application_closed.emit()

    def initialize_theme(self):
        logger.debug("Main Window Controller: initializing theme")
        theme = self.model.settings_model.get_setting("Preferences", "Theme")
        if theme == "Light":
            self.handle_theme_changed(True)
        else:
            self.handle_theme_changed(False)

    def handle_tab_changed(self, index):
        logger.debug(f"Tab changed to index {index}")
        self.tab_changed.emit(index)

    def handle_theme_changed(self, is_light_mode: bool) -> None:
        """
        Handles theme change by applying the appropriate stylesheet

        :param is_light_mode: True if light mode, False if dark mode
        :return: None
        """
        theme_name = "light_theme.qss" if is_light_mode else "dark_theme.qss"
        stylesheet_path = os.path.join(
            application_path, "resources", "GUI_files", "styles", theme_name
        )

        with open(stylesheet_path, "r", encoding="utf-8") as f:
            stylesheet = f.read()
            QApplication.instance().setStyleSheet(stylesheet)
            self.theme_changed.emit(is_light_mode)

    def initialize_language(self):
        """Initialize application language based on stored preference"""
        logger.debug("Main Window Controller: initializing language")
        language = self.model.settings_model.get_setting("Preferences", "Language")
        self.set_application_language(language)

    def set_application_language(self, language):
        """
        Set the application language by loading the appropriate translation file

        :param language: The language to set (e.g., "English", "Spanish")
        """
        logger.debug(f"Setting application language to: {language}")

        app = QApplication.instance()

        if language.lower() == "english":
            logger.debug("Setting language to English (default)")
            self._translator = None
            self.retranslate_all_ui()
            self.language_changed.emit(language)
            return

        # Handle other languages: Load and install translator
        self._translator = QTranslator()

        language_code_map = {
            "english": "en",
            "spanish": "es",
        }
        language_code = language_code_map.get(language.lower(), "en")

        translation_path = os.path.join(
            application_path,
            "resources",
            "GUI_files",
            "translations",
            f"{language_code}.qm",
        )

        # Fallback path check
        if not os.path.exists(translation_path):
            logger.warning(f"Translation file not found at path: {translation_path}")
            return

        if self._translator is not None:
            if self._translator.load(translation_path):
                app.installTranslator(self._translator)
                logger.info(
                    f"Successfully loaded and installed translation for {language}"
                )
            else:
                logger.error(f"Failed to load translation file: {translation_path}")

        self.retranslate_all_ui()

        # Emit the signal after retranslating
        self.language_changed.emit(language)

    def retranslate_all_ui(self):
        """Helper method to call retranslateUi on all relevant UI components."""
        logger.debug("Retranslating all UI components.")

        if hasattr(self.view, "retranslateUi"):
            logger.debug("Calling retranslateUi on main view")
            self.view.retranslateUi(self.view)
        else:
            logger.warning("Main view does not have retranslateUi method")

        if hasattr(self.view, "GeneralTabWidget") and hasattr(
            self.view.GeneralTabWidget.view, "retranslateUi"
        ):
            logger.debug("Calling retranslateUi on GeneralTabWidget")
            self.view.GeneralTabWidget.view.retranslateUi(
                self.view.GeneralTabWidget.view
            )
        else:
            logger.warning(
                "GeneralTabWidget view missing or lacks retranslateUi method"
            )

        if hasattr(self.view, "VisualizationTabWidget") and hasattr(
            self.view.VisualizationTabWidget.view, "retranslateUi"
        ):
            logger.debug("Calling retranslateUi on VisualizationTabWidget")
            self.view.VisualizationTabWidget.view.retranslateUi(
                self.view.VisualizationTabWidget.view
            )
        else:
            logger.warning(
                "VisualizationTabWidget view missing or lacks retranslateUi method"
            )

        if hasattr(self.view, "HelpTabWidget") and hasattr(
            self.view.HelpTabWidget.view, "retranslateUi"
        ):
            logger.debug("Calling retranslateUi on HelpTabWidget")
            self.view.HelpTabWidget.view.retranslateUi(self.view.HelpTabWidget.view)
        else:
            logger.warning("HelpTabWidget view missing or lacks retranslateUi method")

        if hasattr(self.view, "FeedbackTabWidget") and hasattr(
            self.view.FeedbackTabWidget.view, "retranslateUi"
        ):
            logger.debug("Calling retranslateUi on FeedbackTabWidget")
            self.view.FeedbackTabWidget.view.retranslateUi(
                self.view.FeedbackTabWidget.view
            )
        else:
            logger.warning(
                "FeedbackTabWidget view missing or lacks retranslateUi method"
            )

        if hasattr(self.view, "GeneralTabWidget") and hasattr(
            self.view.GeneralTabWidget.controller, "settingsWidget"
        ):
            settings_widget_instance = (
                self.view.GeneralTabWidget.controller.settingsWidget
            )
            if settings_widget_instance and hasattr(
                settings_widget_instance.view, "retranslateUi"
            ):
                logger.debug("Calling retranslateUi on settings widget")
                settings_widget_instance.view.retranslateUi(
                    settings_widget_instance.view
                )
            else:
                logger.warning(
                    "Settings widget view missing or lacks retranslateUi method"
                )
        else:
            logger.warning(
                "GeneralTabWidget controller missing or lacks settingsWidget"
            )


# Model: The app model handles APPLICATION WIDE STATE.
class AppModel(QObject):
    def __init__(self):
        super().__init__()
        self.databases_model = databasesModel()
        self.calculation_model = calculationModel()
        self.settings_model = SettingsModel()
        self.import_manager = ImportManager()
        self.export_manager = ExportManager()

    def setup_models(self, main_window_controller):
        logger.debug("Main Window Model: Setting up models in AppModel")
        main_window_controller.update_progress(30, "Setting up database models...")
        self.databases_model.set_controller(main_window_controller)

        main_window_controller.update_progress(45, "Setting up calculation models...")
        self.calculation_model.set_controller(main_window_controller)

        main_window_controller.update_progress(50, "Loading settings...")
        self.settings_model.set_controller(main_window_controller)

        main_window_controller.update_progress(60, "Setting up import manager...")
        self.import_manager.set_controller(main_window_controller)

        main_window_controller.update_progress(75, "Setting up export manager...")
        self.export_manager.set_controller(main_window_controller)


# View: controls the UI for the Main Window
class MainWindowView(QMainWindow, Ui_MainWindow):
    main_window_closed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setup_icon()

    def setup_icon(self):
        if sys.platform.startswith("win"):  # windows
            icon_file = "icon.ico"
        elif sys.platform.startswith("darwin"):  # macOS
            icon_file = "icon.icns"
        else:  # Linux and other Unix-like systems
            icon_file = "icon.png"

        icon_path = os.path.join(application_path, "resources", "assets", icon_file)

        if not os.path.exists(icon_path):
            icon_path = os.path.join(
                application_path, "resources", "assets", "icon.png"
            )

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            logger.warning(f"Icon file not found at {icon_path}")

    def setup_tabs(self, model, controller):
        # ui elements are defined in UI and referenced in code through
        # a pythonic way of object names with dot-attributes.
        # self.stackedWidget was named that in Qt Designer.

        # Reference objects directly by their object name
        self.GeneralTabWidget = GeneralTabWidget(model, controller)
        self.VisualizationTabWidget = VisualizationTabWidget(model, controller)
        self.HelpTabWidget = HelpTabWidget(model, controller)
        self.FeedbackTabWidget = FeedbackTabWidget(model, controller)

        self.stackedWidget.insertWidget(0, self.GeneralTabWidget.view)
        self.stackedWidget.insertWidget(1, self.VisualizationTabWidget.view)
        self.stackedWidget.insertWidget(2, QWidget())  # TODO: AI CHAT
        self.stackedWidget.insertWidget(3, self.HelpTabWidget.view)
        self.stackedWidget.insertWidget(4, self.FeedbackTabWidget.view)

        # set default to the general widget
        self.stackedWidget.setCurrentWidget(self.GeneralTabWidget.view)

        self.menuGeneral.addAction("General").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.GeneralTabWidget.view)
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
            lambda: self.stackedWidget.setCurrentWidget(self.HelpTabWidget.view)
        )
        self.menuFeedback.addAction("Feedback").triggered.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.FeedbackTabWidget.view)
        )

    def closeEvent(self, event):
        self.main_window_closed.emit()
        event.accept()
        logger.info("Main Window View: Closing...")


# Widget: Ties the View, Controller, and Model together
class MainWindowWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # These comments are here so that I don't get stripped up lol.

        # Initialize all components
        self.model = AppModel()
        self.view = MainWindowView()
        self.controller = MainWindowController(self.model, self.view)
        # Step 1: Starting application
        self.controller.update_progress(0, "Starting application...")

        # Step 2: Setting up user interface
        self.controller.update_progress(15, "Setting up user interface...")
        self.view.setup_tabs(self.model, self.controller)

        # Step 3: Setting up backend models
        self.controller.update_progress(25, "Setting up backend models...")

        # Steps 4-6: Setting up models (database, calculation, settings)
        self.model.setup_models(self.controller)

        # Step 7: Connecting components
        self.controller.connect_signals()

        # Step 8: Applying theme
        self.controller.update_progress(85, "Applying theme...")
        self.controller.initialize_theme()

        # Step 8.5: Initialize language
        self.controller.update_progress(90, "Setting application language...")
        self.controller.initialize_language()

        # Step 9: Sending initialization signal
        self.controller.update_progress(95, "Sending initialization signal...")
        self.controller.send_initialization_signal()

        # Step 10: Ready - final step
        self.controller.update_progress(100, "Ready")
        self.controller.progress_complete.emit()

        self.view.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindowWidget()
    sys.exit(app.exec())

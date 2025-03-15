import logging

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from src.ui.generated_python_ui.ui_visualizationTabWidget import (
    Ui_visualizationTab,
)

logger = logging.getLogger("ui")


class VisualizationTabController(QObject):
    update_requested = Signal()

    def __init__(self, model, view, application_controller):
        super().__init__()
        self.application_controller = application_controller
        self.model = model
        self.view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.update_requested.connect(self.handle_visualization_update)
        self.model.databases_model.calculation_logged.connect(
            self.handle_visualization_update
        )

    def handle_visualization_update(self):
        pass


class VisualizationTabModel:
    def __init__(self, application_model):
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model

    def update_visualization_model_params(self):
        # TODO: Implement UI elements for params collection
        pass


class VisualizationTabView(QWidget, Ui_visualizationTab):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupVisualizationGraph()
        logger.debug("Visualization Tab View: UI setup complete")

    def setupVisualizationGraph(self):
        pass  # TODO: implement data check for this function

    def update_plot(self, data, title="Emissions Graph", arguments=None):
        pass
        # TODO: add parameters to change figure type


class VisualizationTabWidget(QWidget):
    def __init__(self, application_model, application_controller):
        super().__init__()
        self.application_controller = application_controller
        self.application_model = application_model
        self.model = VisualizationTabModel(self.application_model)
        self.view = VisualizationTabView()
        self.controller = VisualizationTabController(
            self.model, self.view, self.application_controller
        )

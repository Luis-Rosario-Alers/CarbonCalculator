import logging

import plotly.express as px
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


class VisualizationTabModel:
    def __init__(self, application_model):
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model
        # TODO: add settings instance here for changes on visualization based on settings


class VisualizationTabView(QWidget, Ui_visualizationTab):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupVisualizationGraph()
        logger.debug("Visualization Tab View: UI setup complete")

    def setupVisualizationGraph(self):
        fig = px.line(
            data_frame=[(3, 10), (2, 5), (1, 3)],
            title="Emissions Graph",
        )
        fig.show()


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

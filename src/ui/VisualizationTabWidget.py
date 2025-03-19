import logging

import pandas as pd
from pyqtgraph import DateAxisItem
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from src.ui.generated_python_ui.ui_visualizationTabWidget import (
    Ui_visualizationTab,
)

logger = logging.getLogger("ui")


class VisualizationTabController(QObject):

    def __init__(self, model, view, application_controller):
        super().__init__()
        self.application_controller = application_controller
        self.model = model
        self.view = view
        self.update_pending = True
        self.emissions_unit = None
        self.user_id = None
        self.fuel_type = None
        self.__connect_signals()

    def __connect_signals(self):
        self.model.databases_model.calculation_logged.connect(
            self.handle_pending_update
        )
        self.application_controller.tab_changed.connect(
            self.handle_tab_changed
        )

        self.application_controller.view.GeneralTabWidget.controller.combobox_information.connect(
            self.handle_initialization_of_settings_comboboxes
        )

        # NOTE: Please keep the order of these signals because they rely on the sequence in which they are connected.
        self.view.emissionsUnitComboBox.currentIndexChanged.connect(
            self.handle_filter_changed
        )

        self.view.fuelTypeComboBox.currentIndexChanged.connect(
            self.handle_filter_changed
        )

        self.view.userIDLineEdit.textChanged.connect(
            self.handle_filter_changed
        )

    def handle_update_visualization(self):
        def plot_data(data=None, user_id="", color=""):  # helper function
            emissions = []
            timestamps = []
            for data_points in data:
                # convert time to int
                timestamp_str = data_points[7]
                timestamp_dt = pd.to_datetime(timestamp_str)
                timestamp_num = timestamp_dt.timestamp()

                emissions.append(data_points[3])
                timestamps.append(timestamp_num)
            data_frame = pd.DataFrame(
                {"time": timestamps, "emissions": emissions}
            )
            self.view.update_plot_units(self.emissions_unit)
            self.view.update_plot(data_frame, color, user_id)
            self.update_pending = False

        if self.update_pending:
            logger.debug(
                "Visualization Tab Controller: Updating Visualization"
            )
            self.emissions_unit = self.view.emissionsUnitComboBox.currentText()
            self.fuel_type = self.view.fuelTypeComboBox.currentText()
            self.user_id = self.view.userIDLineEdit.text()

            if self.user_id:
                logger.debug(
                    "Visualization Tab Controller: user id is selected"
                )
                data = self.model.databases_model.get_emissions_history(
                    emissions_unit=self.emissions_unit,
                    fuel_type=self.fuel_type,
                    user_id=self.user_id,
                )
                plot_data(data=data, user_id=self.user_id)
            else:
                logger.debug(
                    "Visualization Tab Controller: no user id selected"
                )
                user_ids = self.model.databases_model.get_all_user_ids()

                colors = ["r", "g", "b", "c", "m", "y"]
                for i, user_id in enumerate(user_ids):
                    data = self.model.databases_model.get_emissions_history(
                        emissions_unit=self.emissions_unit,
                        fuel_type=self.fuel_type,
                        user_id=str(user_id),
                    )
                    color = colors[i % len(colors)]
                    plot_data(data=data, user_id=user_id, color=color)
            self.update_pending = False
        else:
            logger.debug(
                "Visualization Tab Controller: No update was pending."
            )

    def handle_tab_changed(self, index):
        if (
            index == 1
        ):  # this is the position of the visualization tab on the stacked widget
            self.handle_update_visualization()

    def handle_pending_update(self):
        logger.debug("Visualization Tab Controller: Pending update.")
        self.update_pending = True

    def handle_initialization_of_settings_comboboxes(
        self, fuel_types, calculation_units
    ):
        logger.debug(
            "Visualization Tab Controller: Initializing settings comboboxes."
        )
        self.view.initialize_settings_comboboxes(fuel_types, calculation_units)

    def handle_filter_changed(self):
        logger.debug("Visualization Tab Controller: Filter changed.")
        self.update_pending = True
        self.view.chartPlotWidget.clear()
        self.handle_update_visualization()


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

    def update_plot(self, data, color, user_id):
        if color:
            self.chartPlotWidget.plot(
                data.time,
                data.emissions,
                name=f"User ID: {user_id}",
                pen=color,
            )
        else:
            self.chartPlotWidget.plot(
                data.time, data.emissions, name=f"User ID: {user_id}"
            )
        # TODO: add parameters to change figure type

    def update_plot_units(self, unit):
        """
        :param unit: Measurement unit (Milligrams, Grams, Kilograms, and Metric Tons)
        :return: None
        """
        # FIXME: Fix bug that causes milligrams to have weird name formatting on the Y Axis
        if unit == "Milligrams":
            date_axis = DateAxisItem(orientation="bottom")
            self.chartPlotWidget.setAxisItems({"bottom": date_axis})

            self.chartPlotWidget.setLabel("left", "Emissions (mgCO₂e)")
            self.chartPlotWidget.setTitle("Emissions Over Time")
        elif unit == "Grams":
            date_axis = DateAxisItem(orientation="bottom")
            self.chartPlotWidget.setAxisItems({"bottom": date_axis})

            self.chartPlotWidget.setLabel("left", "Emissions (gCO₂e)")
            self.chartPlotWidget.setTitle("Emissions Over Time")
        elif unit == "Kilograms":
            date_axis = DateAxisItem(orientation="bottom")
            self.chartPlotWidget.setAxisItems({"bottom": date_axis})

            self.chartPlotWidget.setLabel("left", "Emissions (kgCO₂e)")
            self.chartPlotWidget.setTitle("Emissions Over Time")
        elif unit == "Metric Tons":
            date_axis = DateAxisItem(orientation="bottom")
            self.chartPlotWidget.setAxisItems({"bottom": date_axis})

            self.chartPlotWidget.setLabel("left", "Emissions (tCO₂e)")
            self.chartPlotWidget.setTitle("Emissions Over Time")

    def initialize_settings_comboboxes(self, fuel_types, calculation_units):
        logger.debug("Visualization Tab View: initializing combo boxes")
        self.emissionsUnitComboBox.blockSignals(True)
        self.fuelTypeComboBox.blockSignals(True)

        self.emissionsUnitComboBox.addItems(calculation_units)
        self.fuelTypeComboBox.addItems(fuel_types)

        self.emissionsUnitComboBox.blockSignals(False)
        self.fuelTypeComboBox.blockSignals(False)
        logger.debug(
            f"Visualization Tab View: {self.emissionsUnitComboBox.count()}"
        )
        logger.debug(
            f"Visualization Tab View: {self.fuelTypeComboBox.count()}"
        )


class VisualizationTabWidget(QWidget):
    def __init__(
        self, application_model: object, application_controller: object
    ) -> None:
        super().__init__()
        self.application_controller = application_controller
        self.application_model = application_model
        self.model = VisualizationTabModel(self.application_model)
        self.view = VisualizationTabView()
        self.controller = VisualizationTabController(
            self.model, self.view, self.application_controller
        )

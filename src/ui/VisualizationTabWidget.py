import logging

import pandas as pd
from pyqtgraph import DateAxisItem, mkPen
from PySide6.QtCore import QObject
from PySide6.QtGui import QFont
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

        self.application_controller.theme_changed.connect(
            self.view.set_background_for_plot
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

    def handle_update_plot(self):
        """
        Handles visualization by either plotting a single user_id graph line
        or plotting multiple lines of different user_ids.
        """

        def apply_plot_data(
            data=None, user_id="", color=""
        ):  # helper function
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
                apply_plot_data(data=data, user_id=self.user_id)
            else:
                logger.debug(
                    "Visualization Tab Controller: no user id selected"
                )
                user_ids = self.model.databases_model.get_all_user_ids()

                colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ] * ((len(user_ids) + 9) // 10)
                for i, user_id in enumerate(user_ids):
                    data = self.model.databases_model.get_emissions_history(
                        emissions_unit=self.emissions_unit,
                        fuel_type=self.fuel_type,
                        user_id=str(user_id),
                    )
                    color = colors[i % len(colors)]
                    apply_plot_data(data=data, user_id=user_id, color=color)
            self.update_pending = False
        else:
            logger.debug(
                "Visualization Tab Controller: No update was pending."
            )

    def handle_tab_changed(self, index):
        """
        Updates plot when accessing the visualization tab
        """
        if (
            index == 1
        ):  # this is the position of the visualization tab on the stacked widget
            self.handle_update_plot()

    def handle_pending_update(self):
        """
        Handles changing update state for plot
        """
        logger.debug("Visualization Tab Controller: Pending update.")
        self.update_pending = True

    def handle_initialization_of_settings_comboboxes(
        self, combobox_information
    ):
        """
        Handles all initialization jobs for comboboxes
        :param combobox_information: contains information like temp scales, fuel types, etc.
        """
        logger.debug(
            "Visualization Tab Controller: Initializing settings comboboxes."
        )
        # load comboboxes with values
        self.view.initialize_settings_comboboxes(
            combobox_information["fuel_types"],
            combobox_information["calculation_units"],
        )

        # load all user preferences
        preferred_calc_unit = self.model.settings_model.get_setting(
            "Preferences", "Calculation Unit of Measurement"
        )
        self.view.apply_user_preferences(preferred_calc_unit)

    def handle_filter_changed(self):
        logger.debug("Visualization Tab Controller: Filter changed.")
        self.update_pending = True
        self.view.chartPlotWidget.clear()
        self.handle_update_plot()


class VisualizationTabModel:
    def __init__(self, application_model):
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model
        self.settings_model = self.application_model.settings_model

    def update_visualization_model_params(self):
        # TODO: Implement UI elements for params collection
        pass


class VisualizationTabView(QWidget, Ui_visualizationTab):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.color_cache = {}

    def set_background_for_plot(self, is_light_mode: bool):
        if is_light_mode:
            self.chartPlotWidget.setBackground(
                "white"
            )  # White background for light mode

            self.chartPlotWidget.showGrid(x=True, y=True, alpha=0.3)

            bottom_axis = self.chartPlotWidget.getAxis("bottom")
            left_axis = self.chartPlotWidget.getAxis("left")

            text_color = "#212529"  # Dark text for light mode
            font = QFont("Helvetica", 10)

            bottom_axis.setTextPen(text_color)
            left_axis.setTextPen(text_color)

            bottom_axis.setTickFont(font)
            left_axis.setTickFont(font)

            bottom_axis.setStyle(tickTextOffset=10)
            left_axis.setStyle(tickTextOffset=10)

            axis_pen = mkPen(color=text_color, width=1)
            bottom_axis.setPen(axis_pen)
            left_axis.setPen(axis_pen)
        else:
            self.chartPlotWidget.setBackground(
                "black"
            )  # Black background for dark mode

            self.chartPlotWidget.showGrid(x=True, y=True, alpha=0.3)

            bottom_axis = self.chartPlotWidget.getAxis("bottom")
            left_axis = self.chartPlotWidget.getAxis("left")

            text_color = "#F8F9FA"  # Light text for dark mode
            font = QFont("Helvetica", 10)

            bottom_axis.setTextPen(text_color)
            left_axis.setTextPen(text_color)

            bottom_axis.setTickFont(font)
            left_axis.setTickFont(font)

            bottom_axis.setStyle(tickTextOffset=10)
            left_axis.setStyle(tickTextOffset=10)

            axis_pen = mkPen(color=text_color, width=1)
            bottom_axis.setPen(axis_pen)
            left_axis.setPen(axis_pen)

    def update_plot(self, data, color, user_id):
        if color:
            self.chartPlotWidget.plot(
                data.time,
                data.emissions,
                name=f"User ID: {user_id}",
                pen=color,
            )
            self.color_cache.update({user_id: color})
        else:
            if len(self.color_cache) >= 1:
                self.chartPlotWidget.plot(
                    data.time,
                    data.emissions,
                    name=f"User ID: {user_id}",
                    pen=self.color_cache.get(int(user_id)),
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

    def apply_user_preferences(self, user_preferences):
        preferred_calc_unit = user_preferences
        self.emissionsUnitComboBox.blockSignals(True)
        self.emissionsUnitComboBox.setCurrentText(preferred_calc_unit)
        self.emissionsUnitComboBox.blockSignals(False)


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

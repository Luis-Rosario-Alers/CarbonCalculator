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
        Handles visualization by either plotting a single plot_user_id graph line
        or plotting multiple lines of different user_ids.
        """
        if not self.update_pending:
            logger.debug(
                "Visualization Tab Controller: No update was pending."
            )
            return

        logger.debug("Visualization Tab Controller: Updating Visualization")
        # Clear previous plots
        self.view.hide_all_plots()
        self._prepare_visualization_parameters()

        if self.user_id:
            self._plot_single_user_data()
        else:
            self._plot_multiple_users_data()

        self.update_pending = False

    def _prepare_visualization_parameters(self):
        """Extract visualization parameters from the UI."""
        self.emissions_unit = self.view.emissionsUnitComboBox.currentText()
        self.fuel_type = self.view.fuelTypeComboBox.currentText()
        self.user_id = str(self.view.userIDLineEdit.text())
        # Update plot units once at the beginning
        self.view.update_plot_units(self.emissions_unit)

    def _plot_single_user_data(self):
        """Plot emissions data for a single user."""
        logger.debug("Visualization Tab Controller: user id is selected")

        data = self._get_emissions_data(user_id=self.user_id)
        data_frame = self._transform_data_to_dataframe(data)

        color = self.view.color_cache.get(self.user_id, None)
        if color:
            pass
        else:
            color = None
        self.view.update_plot(data_frame, color, self.user_id)
        self.view.show_plot(self.user_id)

    def _plot_multiple_users_data(self):
        """Plot emissions data for all users."""
        logger.debug("Visualization Tab Controller: no user id selected")
        user_ids = self.model.databases_model.get_all_user_ids()

        for user_id in user_ids:
            # Check if we need to update this user's data based on filter changes
            data = self._get_emissions_data(user_id=user_id)
            data_frame = self._transform_data_to_dataframe(data)

            # Use existing color if available
            color = self.view.color_cache.get(user_id, None)
            if not color:
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
                ]
                idx = len(self.view.color_cache) % len(colors)
                color = colors[idx]

            self.view.update_plot(data_frame, color, user_id)
            self.view.show_plot(user_id)

    def _get_emissions_data(self, user_id):
        """Get emission data with caching"""
        # Ensure user_id is a string for consistent cache keys
        cache_key = (user_id, self.fuel_type, self.emissions_unit)
        # Check if we have cached data
        if cache_key in self.model.data_cache:
            logger.debug(
                f"Visualization Tab Controller: Cache hit for user {user_id}"
            )
            return self.model.data_cache[cache_key]
        # No cache hit, fetch from a database
        logger.debug(
            f"Visualization Tab Controller: Cache miss for user {user_id}, fetching data"
        )
        data = self.model.databases_model.get_emissions_history(
            emissions_unit=self.emissions_unit,
            fuel_type=self.fuel_type,
            user_id=user_id,
        )
        # Cache the result
        self.model.data_cache[cache_key] = data
        return data

    @staticmethod
    def _transform_data_to_dataframe(data_points):
        """
        Transform raw emission data into a pandas DataFrame for plotting.
        :param data_points: X and Y data points. (Emissions over Time)
        :return: nothing
        """

        emissions = []
        timestamps = []

        for data_point in data_points:
            # convert time to int
            timestamp_str = data_point[7]
            timestamp_dt = pd.to_datetime(timestamp_str)
            timestamp_num = timestamp_dt.timestamp()

            emissions.append(data_point[3])
            timestamps.append(timestamp_num)

        return pd.DataFrame({"time": timestamps, "emissions": emissions})

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
        preferred_user_id = str(
            self.model.settings_model.get_setting("Preferences", "User ID")
        )
        self.view.apply_user_preferences(
            [preferred_calc_unit, preferred_user_id]
        )  # List user preferences

    def handle_filter_changed(self):
        """
        Efficiently handle filter changes by determining if plots need redrawing
        or just visibility changes.
        """
        logger.debug("Visualization Tab Controller: Filter changed.")

        # Store previous filter values to detect changes
        prev_emissions_unit = self.emissions_unit
        prev_fuel_type = self.fuel_type
        prev_user_id = self.user_id

        # Update current filter parameters
        self._prepare_visualization_parameters()

        # Check if units or fuel type changed - these require redrawing plots
        if (
            prev_emissions_unit != self.emissions_unit
            or prev_fuel_type != self.fuel_type
        ):
            # Units or fuel type changed - redraw everything
            logger.debug(
                "Visualization Tab Controller: Units or fuel type changed - redrawing plots"
            )
            self.view.clear_plots()  # Add this method to the view
            self.model.invalidate_data_cache(
                emissions_unit=prev_emissions_unit, fuel_type=prev_fuel_type
            )
            self.update_pending = True
            self.handle_update_plot()
            return

        # Only user ID filter changed - use visibility to optimize
        if prev_user_id != self.user_id:
            logger.debug(
                "Visualization Tab Controller: Only user ID filter changed"
            )
            self.view.hide_all_plots()

            if self.user_id:
                # Show only the selected user's plot
                if self.user_id in self.view.plot_items:
                    # Plot exists, make it visible
                    logger.debug(
                        f"Visualization Tab Controller: Showing existing plot for user {self.user_id}"
                    )
                    self.view.show_plot(self.user_id)
                else:
                    # Need to create just this one plot
                    logger.debug(
                        f"Visualization Tab Controller: Creating new plot for user {self.user_id}"
                    )
                    self._plot_single_user_data()
            else:
                # No user ID filter - show all plots
                logger.debug("Visualization Tab Controller: Showing all plots")
                self.view.show_all_plots()


class VisualizationTabModel:
    def __init__(self, application_model):
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model
        self.settings_model = self.application_model.settings_model
        self.data_cache = {}

    def update_visualization_model_params(self):
        # TODO: Implement UI elements for params collection
        pass

    # Instead of clearing the entire cache, provide a way to selectively invalidate
    def invalidate_data_cache(
        self, user_id=None, fuel_type=None, emissions_unit=None
    ):
        """
        Invalidate specific cache entries based on parameters.
        If no parameters are provided, invalidates all cache entries.
        """
        if user_id is None and fuel_type is None and emissions_unit is None:
            self.data_cache.clear()
            logger.debug(
                "Visualization Tab Model: All data cache invalidated."
            )
            self.is_cache_valid = False
            return

        keys_to_remove = []
        for key in list(self.data_cache.keys()):
            cached_user_id, cached_fuel_type, cached_emissions_unit = key
            if (
                (user_id is not None and cached_user_id == user_id)
                or (fuel_type is not None and cached_fuel_type == fuel_type)
                or (
                    emissions_unit is not None
                    and cached_emissions_unit == emissions_unit
                )
            ):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.data_cache[key]

        logger.debug(
            f"Visualization Tab Model: {len(keys_to_remove)} cache entries invalidated."
        )


class VisualizationTabView(QWidget, Ui_visualizationTab):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plot_items = {}
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
        # Check if we already have a plot for this user
        if user_id in self.plot_items:
            # Update existing plot data
            self.plot_items[user_id].setData(data.time, data.emissions)
            return

        if not color:
            color = self.color_cache.get(
                user_id, "#1f77b4"
            )  # Default color if wasn't specified

        plot_item = self.chartPlotWidget.plot(
            data.time,
            data.emissions,
            name=f"User ID: {user_id}",
            pen=color,
        )

        # Store the plot item for future reference
        self.plot_items[str(user_id)] = plot_item
        self.color_cache[str(user_id)] = color

    def hide_all_plots(self):
        """
        Hide all plots without removing them
        """
        for plot_item in self.plot_items.values():
            plot_item.setVisible(False)

    def show_plot(self, user_id):
        """
        Show specific plot by user_id
        :param user_id: User ID to show
        """
        if user_id in self.plot_items:
            self.plot_items[user_id].setVisible(True)

    def show_all_plots(self):
        """Show all plots"""
        for plot_item in self.plot_items.values():
            plot_item.setVisible(True)

    def clear_plots(self):
        """
        Remove all plots from the chart widget and reset tracking collections
        """
        for plot_item in self.plot_items.values():
            self.chartPlotWidget.removeItem(plot_item)
        self.plot_items.clear()
        # Keep color_cache for consistent colors between sessions

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
        preferred_calc_unit, preferred_user_id = user_preferences
        self.emissionsUnitComboBox.blockSignals(True)
        self.userIDLineEdit.blockSignals(True)
        self.emissionsUnitComboBox.setCurrentText(preferred_calc_unit)
        self.userIDLineEdit.setText(preferred_user_id)
        self.userIDLineEdit.blockSignals(False)
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

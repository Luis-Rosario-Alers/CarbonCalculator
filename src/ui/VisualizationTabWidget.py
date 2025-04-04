import logging

import pandas as pd
from pyqtgraph import DateAxisItem, mkPen
from PySide6.QtCore import QObject
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget

from ui.generated_python_ui.ui_visualizationTabWidget import Ui_visualizationTab

logger = logging.getLogger("ui")


class VisualizationTabController(QObject):

    def __init__(self, model, view, application_controller):
        super().__init__()
        self.application_controller = application_controller
        self.model = model
        self.view = view

        # State tracking
        self.update_pending = True

        # Parameter defaults
        self.emissions_unit = None
        self.user_id = None
        self.fuel_type = None
        self.start_time = None
        self.end_time = None

        try:
            if hasattr(self.view, "emissionsUnitComboBox"):
                self.emissions_unit = self.view.emissionsUnitComboBox.currentText()
            if hasattr(self.view, "fuelTypeComboBox"):
                self.fuel_type = self.view.fuelTypeComboBox.currentText()
            if hasattr(self.view, "userIDLineEdit"):
                self.user_id = str(self.view.userIDLineEdit.text()).strip()
            if hasattr(self.view, "startTimeFrameDataTimeEdit"):
                self.start_time = self.view.startTimeFrameDataTimeEdit.dateTime()
            if hasattr(self.view, "endTimeFrameDataTimeEdit"):
                self.end_time = self.view.endTimeFrameDataTimeEdit.dateTime()
        except Exception as e:
            logger.warning(f"Could not initialize values from UI: {str(e)}")

        # Connect UI signals
        self.__connect_signals()

    def __connect_signals(self):
        self.model.databases_model.calculation_logged.connect(
            self._handle_pending_update
        )
        self.application_controller.tab_changed.connect(self._handle_tab_changed)

        self.application_controller.view.GeneralTabWidget.controller.combobox_information.connect(
            self._handle_initialization_of_settings_comboboxes
        )

        self.application_controller.theme_changed.connect(
            self.view.set_background_for_plot
        )

        self.application_controller.model.import_manager.import_completed.connect(
            self._handle_pending_update
        )

        # NOTE: Please keep the order of these signals because they rely on the sequence in which they are connected.
        # and I'm not gonna lie I really don't know why but IT WILL GET FIXED.. I promise.
        self.view.emissionsUnitComboBox.currentIndexChanged.connect(
            self._handle_unit_changed
        )

        self.view.fuelTypeComboBox.currentIndexChanged.connect(
            self._handle_unit_changed
        )

        self.view.userIDLineEdit.textChanged.connect(self._handle_user_id_changed)

        self.view.startTimeFrameDataTimeEdit.dateTimeChanged.connect(
            self._handle_time_changed
        )

        self.view.endTimeFrameDataTimeEdit.dateTimeChanged.connect(
            self._handle_time_changed
        )

    def _handle_translate_widget(self):
        self.view.apply_translation()

    def _handle_update_plot(self):
        """
        Handles visualization by either plotting a single plot_user_id graph line
        or plotting multiple lines of different user_ids.
        """
        if not self.update_pending:
            logger.debug("Visualization Tab Controller: No update was pending.")
            return

        logger.debug("Visualization Tab Controller: Updating Visualization")

        try:
            # Clear previous plots
            self.view.hide_all_plots()

            # Prepare parameters from UI
            self._prepare_visualization_parameters()

            # Validate time range
            if not self._is_valid_time_range():
                logger.warning("Skipping plot update due to invalid time range")
                return

            # Plot data based on user selection
            if self.user_id:
                self._plot_single_user_data()
            else:
                self._plot_multiple_users_data()

            self.update_pending = False
            logger.debug("Visualization update completed successfully")
        except Exception as e:
            logger.error(f"Error updating plot: {str(e)}")

    def _prepare_visualization_parameters(self):
        """
        Extract and validate visualization parameters from the UI.
        """

        try:
            # Get combo box selections
            self.emissions_unit = self.view.emissionsUnitComboBox.currentText()
            self.fuel_type = self.view.fuelTypeComboBox.currentText()

            # Get user ID
            self.user_id = str(self.view.userIDLineEdit.text()).strip()

            # Get time range
            self.start_time = self.view.startTimeFrameDataTimeEdit.dateTime()
            self.end_time = self.view.endTimeFrameDataTimeEdit.dateTime()

            # Update plot units based on selection
            self.view.update_plot_units(self.emissions_unit)

            logger.debug(
                f"Visualization parameters prepared: unit={self.emissions_unit}, "
                f"fuel={self.fuel_type}, user={self.user_id or 'all'}"
            )
        except Exception as e:
            logger.error(f"Error preparing visualization parameters: {str(e)}")
            # Set defaults if there was an error
            self.emissions_unit = self.emissions_unit or "Kilograms"
            self.fuel_type = self.fuel_type or "Gasoline"

    def _plot_single_user_data(self):
        logger.debug(f"Plotting data for single user: {self.user_id}")

        try:
            # Get data for this user with caching
            data = self._get_emissions_data(user_id=self.user_id)

            # Transform to pandas DataFrame for plotting
            data_frame = self._transform_data_to_dataframe(data)

            # Get existing color or use a new one
            color = self.view.color_cache.get(self.user_id)

            # Update plot with the data
            self.view.update_plot(data_frame, color, self.user_id)
            self.view.show_plot(self.user_id)

            logger.debug(f"Successfully plotted data for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error plotting data for user {self.user_id}: {str(e)}")

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
            logger.debug(f"Visualization Tab Controller: Cache hit for user {user_id}")
            return self.model.data_cache[cache_key]

        logger.debug(
            f"Visualization Tab Controller: Cache miss for user {user_id}, fetching data"
        )

        # No cache hit, fetch from a database
        date_time_format = "yyyy-MM-dd HH:mm:ss"

        # Safely handle potentially None datetime values
        start_time_str = (
            self.start_time.toString(date_time_format) if self.start_time else ""
        )
        end_time_str = self.end_time.toString(date_time_format) if self.end_time else ""

        data = self.model.databases_model.get_emissions_history(
            time_frame=[start_time_str, end_time_str],
            emissions_unit=self.emissions_unit,
            fuel_type=self.fuel_type,
            user_id=user_id,
        )

        # Cache the result
        self.model.data_cache[cache_key] = data

        # Update the cached time range
        if not hasattr(self.model, "cached_time_range"):
            self.model.cached_time_range = (self.start_time, self.end_time)
        else:
            # Expand the cached range if needed
            current_start, current_end = self.model.cached_time_range
            new_start = (
                min(self.start_time, current_start)
                if self.start_time and current_start
                else (self.start_time or current_start)
            )
            new_end = (
                max(self.end_time, current_end)
                if self.end_time and current_end
                else (self.end_time or current_end)
            )
            self.model.cached_time_range = (new_start, new_end)

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

    def _handle_tab_changed(self, index):
        """
        Updates plot when accessing the visualization tab
        """
        if (
            index == 1
        ):  # this is the position of the visualization tab on the stacked widget
            self._handle_update_plot()

    def _handle_pending_update(self):
        """
        Handles changing update state for plot
        """
        logger.debug("Visualization Tab Controller: Pending update.")
        self.update_pending = True

    def _handle_initialization_of_settings_comboboxes(self, combobox_information):
        """
        Handles all initialization jobs for comboboxes
        :param combobox_information: contains information like temp scales, fuel types, etc.
        """
        logger.debug("Visualization Tab Controller: Initializing settings comboboxes.")
        # load comboboxes with values
        self.view.initialize_settings_comboboxes(
            combobox_information["fuel_types"],
            combobox_information["calculation_units"],
        )

        # load all user preferences
        preferred_calc_unit = self.model.settings_model.get_setting(
            "Preferences", "Calculation Unit of Measurement"
        )
        self.view.apply_user_preferences(preferred_calc_unit)  # List user preferences

    def _handle_unit_changed(self):
        """
        Handles visualization updates when units change.
        Updates parameters and refreshes the visualization if needed.
        """
        logger.debug("Visualization Tab Controller: Unit changed.")

        prev_emissions_unit = self.emissions_unit
        prev_fuel_type = self.fuel_type

        # update parameters to reflect new changes.
        self._prepare_visualization_parameters()

        # Validate time range
        if not self._is_valid_time_range():
            return

        # Handle units or fuel type changes
        if (
            prev_emissions_unit != self.emissions_unit
            or prev_fuel_type != self.fuel_type
        ):
            logger.debug("Visualization Tab Controller: Units or fuel type changed")
            self.view.clear_plots()
            self.model.invalidate_data_cache(
                emissions_unit=prev_emissions_unit, fuel_type=prev_fuel_type
            )
            self.update_pending = True
            self._handle_update_plot()

    def _handle_time_changed(self):
        """
        Handles visualization updates when the time range changes.
        This method tracks previous time values and should update the visualization
        based on the new time range selection.
        It works with the start_time and end_time
        properties to determine if and how to refresh the data.
        """
        prev_start_time = self.start_time
        prev_end_time = self.end_time

        # Update parameters to reflect new changes
        self._prepare_visualization_parameters()

        # Validate time range using our dedicated validation method
        if not self._is_valid_time_range():
            return

        # Handle time range changes if times have changed
        if prev_start_time != self.start_time or prev_end_time != self.end_time:
            try:
                start_timestamp = self.start_time.toSecsSinceEpoch()  # type: ignore
                end_timestamp = self.end_time.toSecsSinceEpoch()  # type: ignore

                if self._check_if_timerange_needs_reload():
                    logger.debug(
                        "Visualization Tab Controller: Loading new time range data"
                    )
                    self.model.invalidate_timerange_cache()
                    self.update_pending = True
                    self._handle_update_plot()
                else:
                    logger.debug(
                        "Visualization Tab Controller: Adjusting time view only"
                    )

                # Update the chart's visible range
                self.view.chartPlotWidget.setXRange(start_timestamp, end_timestamp)
            except Exception as e:
                logger.error(f"Error updating time range visualization: {str(e)}")

    def _handle_user_id_changed(self):
        """Handles visualization updates when any filter criteria changes."""
        logger.debug("Visualization Tab Controller: Filter changed.")

        prev_user_id = self.user_id

        # update parameters to reflect new changes.
        self._prepare_visualization_parameters()

        if prev_user_id != self.user_id:
            logger.debug(
                f"Visualization Tab Controller: User ID changed to {self.user_id}"
            )
            self.view.hide_all_plots()

            if self.user_id:
                if self.user_id in self.view.plot_items:
                    self.view.show_plot(self.user_id)
                else:
                    self._plot_single_user_data()
            else:
                self.view.show_all_plots()

    def _check_if_timerange_needs_reload(self):
        """
        Determines if the new time range requires loading new data.
        Returns True if new data needs to be loaded, False if current data is enough.
        """
        # If we don't have valid times, we need to reload
        if self.start_time is None or self.end_time is None:
            logger.debug("Time range reload check: Missing start or end time")
            return True

        # If we don't have a cached time range, we need to reload
        if not hasattr(self.model, "cached_time_range"):
            logger.debug("Time range reload check: No cached time range")
            return True

        cached_start, cached_end = self.model.cached_time_range

        # If cached values are None, we need to reload
        if cached_start is None or cached_end is None:
            logger.debug("Time range reload check: Cached range has None values")
            return True

        # If new range extends beyond cached range in either direction, reload
        if self.start_time < cached_start or self.end_time > cached_end:
            logger.debug(
                "Time range reload check: New range extends beyond cached range"
            )
            return True

        # Otherwise, we're zooming in or moving within the cached range
        logger.debug("Time range reload check: Using existing cached data")
        return False

    def _is_valid_time_range(self):
        """
        Validates that both start_time and end_time are set and properly ordered.

        Returns:
            bool: True if the time range is valid, False otherwise
        """
        # Check if both times are set
        if self.start_time is None or self.end_time is None:
            logger.warning("Invalid time range: start_time or end_time is None")
            return False

        # Check if times are properly ordered
        if self.start_time > self.end_time:
            logger.warning("Invalid time range: start time is after end time")
            return False

        return True


class VisualizationTabModel:
    def __init__(self, application_model):
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model
        self.settings_model = self.application_model.settings_model
        self.data_cache = {}

    def invalidate_data_cache(self, user_id=None, fuel_type=None, emissions_unit=None):
        """
        Invalidate specific cache entries based on parameters.
        If no parameters are provided, invalidates all cache entries.
        """
        # If no parameters are provided, invalidate all cache entries
        if user_id is None and fuel_type is None and emissions_unit is None:
            self.data_cache.clear()
            logger.debug("Visualization Tab Model: All data cache invalidated.")
            return

        # If parameters are provided, invalidate specific cache entries
        keys_to_remove = []
        for key in self.data_cache:
            cached_user_id, cached_fuel_type, cached_emissions_unit = key
            if (
                (user_id and cached_user_id == user_id)
                or (fuel_type and cached_fuel_type == fuel_type)
                or (emissions_unit and cached_emissions_unit == emissions_unit)
            ):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.data_cache[key]

        logger.debug(
            f"Visualization Tab Model: {len(keys_to_remove)} cache entries invalidated."
        )

    def invalidate_timerange_cache(self):
        """
        Invalidate the cache due to time range changes.
        """

        self.data_cache.clear()

        logger.debug("Visualization Tab Model: Time range cache invalidated")

    def update_cached_time_range(self, start_time, end_time):
        """
        Update the record of what time range is currently cached.
        """

        self.cached_time_range = (start_time, end_time)


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
        logger.debug(f"Visualization Tab View: {self.emissionsUnitComboBox.count()}")
        logger.debug(f"Visualization Tab View: {self.fuelTypeComboBox.count()}")

    def apply_user_preferences(self, user_preferences):
        preferred_calc_unit = user_preferences
        self.emissionsUnitComboBox.blockSignals(True)
        self.emissionsUnitComboBox.setCurrentText(preferred_calc_unit)
        self.emissionsUnitComboBox.blockSignals(False)

    def apply_translation(self):
        self.retranslateUi(self)


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

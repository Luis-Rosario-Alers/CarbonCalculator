import logging

from PySide6.QtCore import QObject, Signal

from data.data_validator import DataValidator
from data.database import databasesModel

# * EDIT THIS FILE IF YOU NEED TO ADD EXTRA FUNCTIONALITY TO THE EMISSION CALCULATOR.

logger = logging.getLogger("core")


class calculationModel(QObject):
    calculation_completed = Signal()
    calculation_result = Signal(
        int, str, float, float, float, str
    )  # user_id, fuel_type, fuel_used, emissions, temperature, farming_technique

    def __init__(self):
        super().__init__()
        self.main_window_controller = None

    def set_controller(self, controller):
        self.main_window_controller = controller
        self.__connect_signals()

    def __connect_signals(self):
        pass

    def calculate_emissions(
        self,
        user_id: int,
        fuel_type: str,
        fuel_used: float,
        temperature=None,
        temperature_type=None,
        farming_technique=None,
    ):
        """
        Calculate the emissions based on the fuel type, fuel used, and optional temperature data.

        Parameters: user_id (str): The ID of the user. Fuel_type (str): The type of fuel used. Fuel_used (float): The
        amount of fuel used. Temperature (float, optional): The temperature at which the fuel is used. Defaults to None.
        Temperature_type (string, optional): The type of temperatures provided (Celsius, Fahrenheit, Kelvin). Defaults to None.

        Returns:
        tuple: A tuple containing user_id, fuel_type, fuel_used, and calculated emissions.

        Raises:
        ValueError: If any of the inputs are invalid or if the calculated emissions data is invalid.
        """
        data_validator = DataValidator()
        # Validate temperature type and temperature values
        if temperature_type is not None and temperature is not None:
            data_validator.validate_temperature_type(temperature_type)
            data_validator.validate_temperature(temperature, temperature_type)

        fuel_type_emissions_variable = (
            databasesModel.get_fuel_type_emissions_modifier(fuel_type)
        )
        farming_technique_emissions_variable = (
            databasesModel.get_farming_technique_info(
                "emissions_modifier", farming_technique
            )
        )

        # * Check This ⬇️ if emission tests have failed
        if temperature is not None and temperature_type is not None:
            logger.info(
                "Temperature data available, adjusting emissions factor"
            )
            baseline_temperature = {
                "Celsius": 20.0,
                "Fahrenheit": 68.0,
                "Kelvin": 293.15,
            }
            baseline_temperature = (
                baseline_temperature.get(temperature_type, None)
                if temperature_type
                else logger.debug("Invalid temperature type")
            )
            temp_deviation = (
                temperature - baseline_temperature
            ) / baseline_temperature

            adjusted_emissions_factor = fuel_type_emissions_variable * (
                1 + temp_deviation**2
            )
            emissions = (
                fuel_used
                * adjusted_emissions_factor
                * farming_technique_emissions_variable
            )
            if not data_validator.validate_emissions_result(emissions):
                raise ValueError("Invalid emissions data")
            self.calculation_completed.emit()
            self.calculation_result.emit(
                user_id, fuel_type, fuel_used, emissions
            )
            return fuel_type, fuel_used, emissions
        else:
            logger.info(
                "Temperature data not available, using standard emissions factor"
            )
            emissions = (
                fuel_used
                * fuel_type_emissions_variable
                * farming_technique_emissions_variable
            )
            if not data_validator.validate_emissions_result(emissions):
                raise ValueError("Invalid emissions data")
            self.calculation_completed.emit()
            self.calculation_result.emit(
                user_id, fuel_type, fuel_used, emissions, farming_technique
            )
            return fuel_type, fuel_used, emissions, farming_technique

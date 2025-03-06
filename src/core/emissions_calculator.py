import logging

from PySide6.QtCore import QObject, Signal

from data.data_validator import DataValidator
from data.database import databasesModel

# * EDIT THIS FILE IF YOU NEED TO ADD EXTRA FUNCTIONALITY TO THE EMISSION CALCULATOR.

logger = logging.getLogger("core")


class calculationModel(QObject):
    calculation_completed = Signal()
    calculation_result = Signal(
        int, str, float, float, str
    )  # user_id, fuel_type, fuel_used, emissions, farming_technique

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

        Parameters: user_id (str): The ID of the user. fuel_type (str): The type of fuel used. fuel_used (float): The
        amount of fuel used. temperature (float, optional): The temperature at which the fuel is used. Defaults to None.
        temperature_type (int, optional): The type of temperature provided (0 for Celsius, 1 for Fahrenheit,
        2 for Kelvin). Defaults to None.

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

        emissions_factor = databasesModel.get_emissions_factor(fuel_type)

        # * Check This ⬇️ if emission tests have failed
        if temperature is not None and temperature_type is not None:
            logger.info(
                "Temperature data available, adjusting emissions factor"
            )
            baseline_temperature = [
                20.0,  # Celsius
                68.0,  # Fahrenheit
                293.15,  # Kelvin
            ]
            temp_deviation = (
                temperature - baseline_temperature[temperature_type]
            ) / baseline_temperature[temperature_type]

            adjusted_emissions_factor = emissions_factor * (
                1 + temp_deviation**2
            )

            emissions = fuel_used * adjusted_emissions_factor
            if not data_validator.validate_emissions(emissions):
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
            emissions = fuel_used * emissions_factor
            if not data_validator.validate_emissions(emissions):
                raise ValueError("Invalid emissions data")
            self.calculation_completed.emit()
            self.calculation_result.emit(
                user_id, fuel_type, fuel_used, emissions
            )
            return fuel_type, fuel_used, emissions

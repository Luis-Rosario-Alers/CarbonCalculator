import logging

from data.data_validator import DataValidator
from data.database import get_emissions_factor, log_calculation

# * EDIT THIS FILE IF YOU NEED TO ADD EXTRA FUNCTIONALITY TO THE EMISSIONS CALCULATOR.

logger = logging.getLogger("core")


# class to make Emissions calculating easier.
async def calculate_emissions(
    user_id: int,
    fuel_type: str,
    fuel_used: float,
    temperature=None,
    temperature_type=None,
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
    emissions_factor = await get_emissions_factor(fuel_type)

    # * Check This ⬇️ if emissions tests have failed
    if temperature is not None and temperature_type is not None:
        logger.info("Temperature data available, adjusting emissions factor")
        baseline_temperature = [
            15,
            59,
            288.15,
        ]  # Baseline temperatures in Celsius, Fahrenheit, and Kelvin
        temp_deviation = (
            temperature - baseline_temperature[temperature_type]
        ) / baseline_temperature[temperature_type]
        adjusted_emissions_factor = emissions_factor * (1 + temp_deviation**2)
        emissions = fuel_used * adjusted_emissions_factor
        if not data_validator.validate_emissions(emissions):
            raise ValueError("Invalid emissions data")
        await log_calculation(user_id, fuel_type, fuel_used, emissions)
        return user_id, fuel_type, fuel_used, emissions
    else:
        logger.info("Temperature data not available, using standard emissions factor")
        emissions = fuel_used * emissions_factor
        if not data_validator.validate_emissions(emissions):
            raise ValueError("Invalid emissions data")
        await log_calculation(user_id, fuel_type, fuel_used, emissions)
        return user_id, fuel_type, fuel_used, emissions

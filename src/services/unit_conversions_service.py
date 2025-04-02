import logging

logger = logging.getLogger("services")


class UnitConversionsService:
    """
    A service class for converting between different units of measurement.
    """

    # use this for fuels measured in mass
    @staticmethod
    def convert_mass_to_mass(fuel_value, from_unit):
        """
        Converts measurements between different units.
        """

        # Define conversion formulas to convert from unit to Kilograms
        from_unit_conversion_formulas = {
            "Milligrams": lambda x: x / 1_000_000,
            "Grams": lambda x: x / 1000,
            "Kilograms": lambda x: x,
            "Metric Tons": lambda x: x * 1000,
        }

        converted_value = from_unit_conversion_formulas[from_unit](fuel_value)
        # Convert the fuel_value to liters
        logger.debug(f"Converting {fuel_value} {from_unit} to {converted_value} liters")
        return converted_value

    # use this for fuels measured in volume (natural gas, gasoline, etc.)
    @staticmethod
    def convert_volume_to_volume(fuel_value, from_unit):
        """
        Converts measurements between different units.
        """

        # Define conversion formulas to convert from unit to liters
        from_unit_conversion_formulas = {
            "Cubic Meters": lambda x: x * 1000,
            "Liters": lambda x: x,
            "Cubic Feet": lambda x: x * 28.3168,
        }

        # Convert the fuel_value to liters
        logger.debug(f"Converting {fuel_value} {from_unit} to liters")
        converted_value = from_unit_conversion_formulas[from_unit](fuel_value)
        return converted_value

    @staticmethod
    def convert_calculation_result_to_desired_unit(
        calculation_result, calculation_unit
    ):
        """
        Converts the result of the calculation to the desired unit.
        """
        # Define conversion formulas to convert from Kilogram to desired unit
        from_unit_conversion_formulas = {
            "Milligrams": lambda x: x * 1_000_000,
            "Grams": lambda x: x * 1000,
            "Kilograms": lambda x: x,
            "Metric Tons": lambda x: x / 1000,
        }

        converted_emissions_result = from_unit_conversion_formulas[calculation_unit](
            calculation_result
        )
        logger.debug(
            f"Converting {calculation_result} Kilograms to {converted_emissions_result} {calculation_unit}"
        )
        return converted_emissions_result

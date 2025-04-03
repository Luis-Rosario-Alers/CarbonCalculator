import logging

import requests

# EDIT THIS FILE IF YOU NEED TO ALTER THE WEATHER SERVICE

# Weather Service object that has a get_weather method
# to get the weather of current location.
logger = logging.getLogger("services")


class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather_data(
        self, latitude=None, longitude=None
    ) -> tuple[float, float, float] | None:
        logger.info("Fetching weather data")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            weather_data = response.json()
            if weather_data.get("cod") != 200:
                logger.error("API Error: Unable to retrieve weather data")
                logger.error("Weather data not retrieved")
                return None

            logger.info("Weather data retrieved")
            temperature_kelvin = weather_data["main"]["temp"]

            temperature_celsius = self.__kelvin_to_celsius(temperature_kelvin)
            temperature_fahrenheit = self.__kelvin_to_fahrenheit(temperature_kelvin)
            logger.info("Weather data successfully retrieved and processed.")
            return (
                temperature_celsius,
                temperature_fahrenheit,
                temperature_kelvin,
            )
        except requests.RequestException as e:
            logger.error(f"Error getting weather data: {e}")
            return None

    @staticmethod
    def __kelvin_to_celsius(temperature: float):
        celsius = temperature - 273.15
        return celsius

    @staticmethod
    def __kelvin_to_fahrenheit(temperature: float):
        fahrenheit = (temperature - 273.15) * 9 / 5 + 32
        return fahrenheit

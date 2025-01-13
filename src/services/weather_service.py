import logging

import aiohttp

# EDIT THIS FILE IF YOU NEED TO ALTER THE WEATHER SERVICE

# Weather Service object that has a get_weather method
# to get the weather of current location.
logger = logging.getLogger("services")


class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key

    async def get_weather(
        self, latitude=None, longitude=None
    ) -> tuple[float, float, float]:
        logger.info("Fetching weather data")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}"
        timeout = aiohttp.ClientTimeout(total=5)
        try:
            async with aiohttp.ClientSession() as session:
                response = session.get(url, timeout=timeout)
                weather_data = await response.json()
                if weather_data.get("cod") != 200:
                    logger.error(
                        f"API Error: {weather_data.get('message', 'Unknown error')}"
                    )
                    return None

                logger.info("Weather data retrieved")
                temperature_kelvin = weather_data["main"]["temp"]
                temperature_converter = TemperatureConverter(temperature_kelvin)
                temperature_celsius = temperature_converter.convert_to_celsius()
                temperature_fahrenheit = temperature_converter.convert_to_fahrenheit()
                logger.info(
                    f"Temperature in Celsius: {temperature_celsius}, Fahrenheit: {temperature_fahrenheit}, Kelvin: {temperature_kelvin}"
                )
                return temperature_celsius, temperature_fahrenheit, temperature_kelvin
        except aiohttp.ClientError as e:
            logger.error(f"Error getting weather data: {e}")
            return None


# converts temperature from Kelvin to Celsius and Fahrenheit
class TemperatureConverter:
    def __init__(self, temperature):
        self.temperature = temperature

    def convert_to_celsius(self):
        celsius = self.temperature - 273.15
        return celsius

    def convert_to_fahrenheit(self):
        fahrenheit = (self.temperature - 273.15) * 9 / 5 + 32
        return fahrenheit

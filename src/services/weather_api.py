import requests

# EDIT THIS FILE IF YOU NEED TO ALTER THE WEATHER SERVICE


# Weather Service object that has a get_weather method
# to get the weather of current location.
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={self.api_key}"
        )
        timeout = 5
        response = requests.get(url, timeout=timeout)
        weather_data = response.json()
        return weather_data

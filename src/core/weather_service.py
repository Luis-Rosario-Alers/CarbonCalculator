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

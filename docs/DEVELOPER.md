# Developer Documentation

These are the developer docs of the carbon calculator project.

## Start

The `start()` function is in the `main.py` file.

### Purpose

To initialize the database, test the users internet connection, retrive the users location, and fetch the weather data.

It initializes the data bases using the code:

```python
await db.database_initialization()
```

It then tests the user's internet connection using:

```python
await test_user_internet_connection()
```

If required API keys (`WEATHER_API_KEY` and `IP_API_TOKEN`) are missing, or if there is no internet connection, the program will proceed without fetching local temperatures.

```python
if (
   WEATHER_API_KEY is None
   or IP_API_TOKEN is None
   or internet_connection_process is False
):
   logger.warning("Continuing program without local temperatures")
   user_local_temps = None
   return internet_connection_process
```

But if it can find both required API keys then it will retrieve the user's location using the `UserLocationService`:

```python
user_location_service = UserLocationService(IP_API_TOKEN)
user_coords = await user_location_service.get_user_location()
```

After that it fetches weather data for the user's coordinates using the `WeatherService`:

```python
user_local_temps = await weather_service.get_weather(
   user_coords[0],  # latitude
   user_coords[1],  # longitude
)
```

---

## Run Main Window

The `run_main_window` function is in the `main.py` file.

### Purpose

To set up the Qt application and integrate the event loop with `asyncio`, then display the main window of the application.

It creates a `QApplication` instance using the code:

```python
app = QApplication([])
```

It integrates the Qt event loop with `asyncio` using:

```python
loop = QEventLoop(app)
asyncio.set_event_loop(loop)
```

It then creates and displays the main window:

```python
main_window = MainWindow(internet_connection_status_passed)
main_window.show()
```

The function runs the event loop using:

```python
with loop:
   loop.run_forever()
```

---

## Main Window Operations

### Close Event

`closeEvent` is a method inside of the class `MainWindow` in the file `main_window.py`

The `closeEvent` method is triggered when the user attempts to close the application window. Its purpose is to confirm the user's intention to exit and handle the response accordingly.

#### Purpose

The method displays a dialog box asking the user whether they are sure they want to exit the application. This dialog is created using the following code:

```python
reply = QMessageBox.question(
    self,
    "Exit",
    "Are you sure you want to exit?",
    QMessageBox.Yes | QMessageBox.No,
    QMessageBox.No,
)
```

- **Title**: `"Exit"`
- **Message**: `"Are you sure you want to exit?"`
- **Buttons**: `Yes` and `No`, with the default set to `No`.

#### User Response Handling

If the user clicks Yes, the application logs the exit action and closes:

```python
if reply == QMessageBox.Yes:
    logging.getLogger("main").info("Exiting application")
    event.accept()
```

The logger records: `"Exiting application"`.
`event.accept()` allows the application to close.

If the user clicks No, the application ignores the close event and keeps running:

```python
else:
    event.ignore()
```

This makes sure the user does not accidentally exit the program without confirmation.

---

## InputForm Operations

### Receiving the Submit Button Click

When the user clicks the "Submit" button, the `submit` method is triggered through the `clicked` signal of the `submit_button`.

```python
self.submit_button.clicked.connect(self.submit)
```

This establishes that when the button is clicked, the `submit` method will execute.

### Triggering Submit

Inside the `submit` method, user-entered values are retrieved from input fields for processing.

```python
user_id = self.user_id_entry.text()
fuel_type = self.fuel_type_entry.text()
fuel_used = self.fuel_used_entry.text()
```

Here, the inputs are fetched as strings from the GUI components (`user_id_entry`, `fuel_type_entry`, and `fuel_used_entry`).

### Converting user_id to an Integer

The `user_id` input is attempted to be converted to an integer using `int(user_id)`. If this fails, a `ValueError` is caught, and `user_id` is set to `None`.

```python
try:
    user_id = int(user_id)
except ValueError:
    user_id = None
    self.display_error("Invalid User ID. Must be an integer.")
```

This ensures the `user_id` is valid before proceeding.

---

### Converting fuel_used to a Float

The `fuel_used` input is converted to a float. If this fails, a `ValueError` is caught, and `fuel_used` is set to `None`.

```python
try:
    fuel_used = float(fuel_used)
except ValueError:
    fuel_used = None
    self.display_error("Invalid Fuel Used. Must be a number.")
```

This step ensures the `fuel_used` value can be processed as a number input.

---

### Did Conversion Fail?

If either conversion fails, validation cannot proceed. This is determined by checking if `user_id` or `fuel_used` is `None`.

```python
if user_id is None or fuel_used is None:
    return  # Early exit due to invalid inputs
```

An early return prevents further operations when conversions fail.

---

### Validating Inputs Using `DataValidator`

The `DataValidator` validates the inputs (`user_id`, `fuel_type`, `fuel_used`). This ensures all fields are within acceptable ranges and formats.

```python
if not DataValidator.validate_user_id(user_id):
    self.display_error("Invalid User ID.")
    return
if not DataValidator.validate_fuel_type(fuel_type):
    self.display_error("Invalid Fuel Type.")
    return
if not DataValidator.validate_fuel_used(fuel_used):
    self.display_error("Invalid Fuel Used.")
    return
```

Each input is checked, and if any validation fails, an error message is displayed, and the method exits.

---

### Are Any Inputs Invalid?

If any validation check returns `False`, an appropriate error message is logged, and the process terminates.

```python
if not all([user_id, fuel_type, fuel_used]):
    self.display_error("One or more inputs are invalid.")
    return
```

This makes sure that inputs that are invalid don't make it to the next steps.

---

## user_local_temps Equal to None?

`user_local_temps` determines how emissions are calculated.

### If Yes (`user_local_temps` is `None`)

If no temperature data is available, only `user_id`, `fuel_type`, and `fuel_used` are passed to `calculate_emissions`.

```python
if user_local_temps is None:
    emissions = calculate_emissions(user_id, fuel_type, fuel_used)
```

### If No (`user_local_temps` is not `None`)

When temperature data is available, the `temperature_type` method allows the user to select a unit (Celsius, Fahrenheit, or Kelvin), and the corresponding local temperature is included.

```python
else:
    temp_type = self.temperature_type()
    emissions = calculate_emissions(user_id, fuel_type, fuel_used, user_local_temps[temp_type])
```

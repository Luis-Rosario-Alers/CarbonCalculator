# Changelog

## v0.4.1

### Changed

- Changed `loop = asyncio.get_event_loop()` to `loop = asyncio.new_event_loop()` in `main.py` to be able to run the application without any deprecation issues
- Changed logic on how GUI displays application icon to be able to dynamically change format depending on OS


### Added

- Added `determine_application_path()` in `database.py` to be able to dynamically determine the path for database folder creation and other main logic operations
- Added `setup_database_folder()` in `database.py` to be able to create the database folder if it does not exist in a more concise way
- Added GitHub Actions workflow for automated testing

### Fixed

- Fixed bug where the application would not continue to temperature type sequence because of incorrect if statement condition
- Fixed bug where database would not have a connection open because of bad async database operations handling

### Tests

- Fixed tests that were not passing because of bad async integration into main logic

## v0.4.0

### Added

- Added ipinfo and openweathermap API's to provide temperature deviation for `EmissionsCalculator` Class

### Changed

- Updated `requirements.txt` to reflect new dependencies

## v0.3.3

### Added

- Added logging functionality to debug faster
- added qasync to integrate asyncio eventloop with Qt eventloop

### Changed

- Changed Python Qt bindings from PyQt5 to PySide6

## v0.3.2

### Added

- Added Asyncio functionality with GUI

### Fixed

- Issue where the event loop would never end and cause the program to run indefinitely

## v0.3.1

### Added

- Display results after calculation on GUI
- Added more information to the README

### Fixed

- Issue where `DataValidator` class was not being imported properly in multiple files.

## v0.3.0

### Added

- **User Interface:**
  - Implemented a new graphical user interface (GUI) using PyQt5
  - Added input fields for user ID, fuel type, and fuel used in the GUI
  - Created a submit button to trigger emissions calculation from the GUI

## v0.2.0

### Added

- **Data Validation:**
  - Implemented data validation in `inputhandler.get_user_input()` to ensure user inputs are valid
  - Added validation in `EmissionsCalculator.calculate_emissions()` to check for valid user ID, fuel type, and fuel used
  - Added input validation in `EmissionsCalculator.validate_inputs()` to ensure valid data before logging calculations

- **Testing Enhancements:**
  - Created pytest fixture `setup_teardown` for setting up and cleaning databases before and after tests
  - Added tests:
    - `test_negative_user_id_retries` to verify user ID validation and retry logic
    - `test_input_validation_loops_until_valid_data` to confirm input validation loops until valid data is provided
    - `test_no_null_emission_factor` to ensure `fuel_type_check` does not return a `NULL` value
    - Added proper mocking in tests to prevent them from hanging and to make correct assertions
- **Database Management:**
  - Configured longer timeout for SQLite connections in test functions to handle potential locking issues
  - Implemented retry logic in `EmissionsCalculator.log_calculation()` to handle database locking issues
  - Created database cleanup methods in test fixtures to properly close connections and delete the database folder after tests
  - Implemented context managers in database operations to ensure connections are properly closed

- **Import Improvements:**
  - Updated `import_from_csv` method in `ImportManager` to read data once, validate it, and insert data into the database efficiently

### Fixed

- **Permission Errors:**
  - Fixed `PermissionError` by ensuring all database connections are properly closed before attempting to delete the database folder in tests
  - Resolved `PermissionError` and `OperationalError` by ensuring all database connections are closed before attempting to delete the database folder in tests

- **Test Corrections:**
  - Fixed `TypeError` in test functions by using cursors to fetch expected results from the database
  - Fixed `ModuleNotFoundError` in tests by correctly referencing the `fuel_type_check` method within the inputhandler class
  - Fixed `AssertionError` in tests by updating the expected error messages to match the actual error messages in `inputhandler.get_user_input()`
  - Corrected issues where tests were passing too quickly without proper execution

- **Database Errors:**
  - Resolved `sqlite3.ProgrammingError` by moving commits inside the context manager and ensuring connections are managed correctly
  - Fixed `sqlite3.OperationalError` by ensuring proper database connection management and increasing timeout values
  - Fixed `KeyError` in `import_from_csv` by validating data properly and handling missing keys

### Changed

- **Main Application Enhancements:**
  - Updated `main.py` to include data validation and proper user input handling
  - Improved error handling and reporting in test functions
  - Updated `inputhandler.get_user_input()` to ensure user ID is a positive integer and to print "User ID must be a positive integer" for invalid user IDs
  - Updated tests in `test_input_handler.py` to reflect changes in input validation and error messages

- **Code Refactoring:**
  - Updated `log_calculation` in `EmissionsCalculator` to include input validation and retry logic
  - Refactored tests to ensure database connections are properly managed and to handle database locking issues
  - Modified `import_from_csv` in `ImportManager` to improve data validation and error handling
  - Improved error messages and exception handling throughout the application

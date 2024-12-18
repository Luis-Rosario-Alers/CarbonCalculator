# Agricultural Carbon Calculator User Manual

## Introduction

Welcome to the Agricultural Carbon Calculator! This tool is designed to help agricultural businesses measure and track their carbon footprint. By taking into account various farming operations, equipment usage, and agricultural practices, this calculator provides accurate carbon emission estimates.

## Installation

### Steps

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Luis-Rosario-Alers/CarbonCalculator
    cd CarbonCalculator
    ```

2. **Create and Activate a Virtual Environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # or `venv\Scripts\activate` on Windows
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Getting Started

1. **Run the Main Script**:

    ```bash
    python main.py
    ```

2. **Follow the Prompts**:
    - Enter your user ID.
    - Enter the fuel type.
    - Enter the amount of fuel used.

3. **View the Results**:
    - The calculator will display the calculated carbon emissions.

## Features and Usage

### Calculating Emissions

- **User Input**: Enter your user ID, fuel type, and fuel used.
- **Calculation**: The calculator uses predefined emission factors to calculate the carbon emissions based on the input.

### Exporting Data

- **Export to JSON**:
  - After calculating emissions, you can choose to export the data to a JSON file.

  - Follow the prompt to enter the path where you want to save the JSON file.

- **Export to CSV**:
  - You can also export the data to a CSV file.

  - Follow the prompt to enter the path where you want to save the CSV file.

### Importing Data

- **Import from JSON**:
  - You can import data from a JSON file.

  - Follow the prompt to enter the path of the JSON file you want to import.

**JSON Format:**

```json
[
  {
    "user_id": "123",
    "fuel_type": "gasoline",
    "fuel_used": 50,
    "emissions": 120,
    "timestamp": "2023-01-01 10:00:00"
  },
  {
    "user_id": "124",
    "fuel_type": "diesel",
    "fuel_used": 30,
    "emissions": 90,
    "timestamp": "2023-01-02 11:00:00"
  }
]
```

- **Import from CSV**:
  - You can import data from a CSV file.

  - Follow the prompt to enter the path of the CSV file you want to import.

**CSV Format:**

```csv
user_id,fuel_type,fuel_used,emissions,timestamp
123,gasoline,50,120,2023-01-01 10:00:00
124,diesel,30,90,2023-01-02 11:00:00
```

## Troubleshooting

### Common Issues

- **Database Locked Error**:
  - Ensure that no other process is accessing the database.

  - Try increasing the timeout value in the database connection settings.

- **Permission Denied Error**:
  - Ensure you have the necessary permissions to read/write to the specified directory.

  - Check the file path and ensure it is correct.

- **Invalid Input Error**:
  - Ensure that all inputs are in the correct format and within valid ranges.

## Contact and Support

If you encounter any issues or have any questions, please contact us at [luisrosarioalers@gmail.com](luisrosarioalers@gmail.com).

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Contributors

We welcome contributions from the community! Please refer to the [CONTRIBUTORS.md](CONTRIBUTORS.md) file to see the list of contributors and to learn how you can contribute to this project.

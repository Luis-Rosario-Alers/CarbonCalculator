# Agricultural Carbon Calculator User Manual

## Introduction

Welcome to the Agricultural Carbon Calculator! This tool is designed to help agricultural businesses measure and track their carbon footprint. By taking into account various farming operations, equipment usage, and agricultural practices, this calculator provides accurate carbon emission estimates.

## Getting Started

1. Run the executable file `CarbonCalculator.exe` (Windows) or `CarbonCalculator` for macOS and Linux.

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
~  - After calculating emissions, you can choose to export the data to a JSON file.

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

- **invalid file format**
  - Make sure that you put either `.csv` or `.json` at the end of the file name when exporting and importing to avoid this issue.

## Contact and Support

If you encounter any issues or have any questions, dont hesitate to create a github issue.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Contributors

We welcome contributions from the community! Please refer to the [CONTRIBUTING.md](../CONTRIBUTING.md) file to see the list of contributors and to learn how you can contribute to this project.

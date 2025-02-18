# Developer Documentation

## Table of Contents

- [Developer Documentation](#developer-documentation)
  - [Table of Contents](#table-of-contents)
    - [Setup](#setup)
  - [Project Structure](#project-structure)
    - [Auth](#auth)
    - [Core](#core)
    - [Data](#data)
      - [Data Management](#data-management)
      - [Data Processing](#data-processing)
    - [Services](#services)
    - [UI](#ui)
  - [Development Environment](#development-environment)
    - [Contributors' Development Environment Requirements](#contributors-development-environment-requirements)
      - [Common Setup Issues and Solutions](#common-setup-issues-and-solutions)
  - [Development Workflow](#development-workflow)
    - [Branching Strategy](#branching-strategy)
  - [Testing](#testing)
    - [How to run tests](#how-to-run-tests)

### Setup

1. **Fork the repository**:

    - Go to the repository page on GitHub.
    - Click the "Fork" button to create a copy of the repository under your GitHub account.

2. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/CarbonCalculator.git
    cd CarbonCalculator
    ```

3. **Create and activate a virtual environment**:

    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    # source .venv/bin/activate  # On macOS/Linux
    ```

4. **Install the package in editable mode**:

    ```sh
    pip install -e .
    ```

5. **Run the application**:

    ```sh
    carbon_calculator
    ```

## Project Structure

The project follows a modular structure with clear separation of concerns. Here's an overview of the main directories and files under `src/`:

![Project Structure](/docs/images/project_structure.png)

### Auth

![Auth Folder](/docs/images/auth_path.png)

The `auth` folder manages user authentication and authorization:

- `user_auth.py`: Handles user authentication flows and access control
  - User login/logout
  - Permission management
  - Session handling
  (Note: Authentication features are planned but not yet implemented)

### Core

![Core Folder](/docs/images/core_path.png)

The `core` folder contains the main business logic and calculation engine:

- `emissions_calculator.py`: Central carbon emissions calculator
  - Processes temperature data from weather service
  - Applies emissions factors and formulas
- `recommendations.py`: Provides emission reduction recommendations using AI (Not implemented yet)

### Data

![Data Folder](/docs/images/data_path.png)

The `data` folder contains the data management logic for the application:

#### Data Management

- `resources/` - Data files and app configuration
- `database.py` - Database operations (creation, cleanup, etc.)
- `settings_manager.py` - Manages application settings (e.g. default values, etc.)

#### Data Processing

- `data_validator.py` - Input validation
- `export_manager.py` - Data export (CSV, JSON)
- `import_manager.py` - Data import (CSV, JSON)

### Services

![Services Folder](/docs/images/services_path.png)

The `services` folder contains the service logic for the application:

- `weather_service.py` - Weather data retrieval and processing
- `user_location_service.py` - User location retrieval and processing
- `user_internet_connection_service.py` - Tests user internet connection

### UI

![UI Folder](/docs/images/ui_path.png)

The `ui` folder contains the UI logic for the application:

- `main_window.py` - Main application window to initialize the application UI
- `settings_menu.py` - Settings menu for configuring the application
- `input_forms.py` - Input forms such as input fields, buttons, etc.

## Development Environment

### Contributors' Development Environment Requirements

This project enforces the use of pre-commit hooks to ensure adherence to commit standards and maintain code quality.

Follow the steps below to set up pre-commit in your development environment:

1. Ensure you have Python 3.10+ and pip installed.

2. Activate the virtual environment:

   ```bash
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. Install the project's dependencies:

   ```bash
   pip install -e .
   ```

4. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

5. Install the project's pre-commit hooks:

   ```bash
   pre-commit install
   ```

#### Common Setup Issues and Solutions

- **Virtual Environment Activation Fails**:
  - Windows: Ensure you're using PowerShell or CMD with admin privileges
  - Unix: Check file permissions with `ls -la .venv/bin/activate`
  - Try recreating the virtual environment if activation consistently fails

- **Dependency Conflicts**:
  - Clear pip cache: `pip cache purge`
  - Update pip: `python -m pip install --upgrade pip`
  - If conflicts persist, try installing dependencies one by one to identify the conflict

- **Pre-commit Hook Installation Fails**:
  - Ensure git is initialized: `git init`
  - Try removing and reinstalling pre-commit: `pip uninstall pre-commit && pip install pre-commit`

For detailed commit guidelines and instructions on how to contribute, please refer to the [CONTRIBUTING.md](./../CONTRIBUTING.md) file.

## Development Workflow

### Branching Strategy

This project uses the git-flow branching strategy, which provides a robust framework for managing larger projects. The workflow is particularly well-suited for projects that have a scheduled release cycle.

![Git Flow](/docs/images/git_flow_diagram.png)

Key Concepts:

- `main` - Production-ready code
- `develop` - Latest development changes
- `feature/*` - New features
- `bugfix/*` - Non-urgent bug fixes
- `hotfix/*` - Urgent production fixes
- `release/*` - Release preparation

Common Workflows:

1. **Starting a New Feature**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   # Make changes
   git commit -m "Add new feature"
   git push origin feature/new-feature
   # Create PR to develop
   ```

2. **Fixing a Bug**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b bugfix/fix-description
   # Fix bug
   git commit -m "Fix bug"
   git push origin bugfix/fix-description
   # Create PR to develop
   ```

3. **Emergency Hotfix**:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-fix
   # Fix critical issue
   git commit -m "Fix critical issue"
   git push origin hotfix/critical-fix
   # Create PR to both main and develop
   ```

For more detailed information about git-flow, refer to:

- [Atlassian's Git Flow Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Git Flow Cheat Sheet](https://danielkummer.github.io/git-flow-cheatsheet/)

## Testing

### How to run tests

This project uses pytest for testing, with a focus on maintaining high test coverage and ensuring code reliability.

Basic test commands:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=.

# Run specific test file
pytest tests/path/to/test_file.py

# Run tests with detailed output
pytest -v

# Run tests that match a pattern
pytest -k "test_pattern"
```

For more information on pytest, refer to the [pytest documentation](https://docs.pytest.org/en/stable/).

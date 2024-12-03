# Agricultural Carbon Calculator

## Version
Current version: 0.1.0

## Description
Carbon footprint calculator for agricultural businesses.

## Installation
```bash
git clone https://github.com/Luis-Rosario-Alers/CarbonCalculator
cd CarbonCalculator
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
````

## Setting up Pre-commit Hooks

To ensure code quality and consistency, we use pre-commit hooks in this project. Follow the steps below to set up pre-commit hooks:
```bash
1. **Install the required dependencies**:
    pip install -r requirements.txt

2. **Install pre-commit hooks**:
    pre-commit install
````
This will install the pre-commit hooks defined in the `.pre-commit-config.yaml` file. Every time you make a commit, the hooks will run automatically to check your code.
These are the standard hooks you should be using for this project.
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.1
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: [ "--configfile", ".bandit.yaml" ]

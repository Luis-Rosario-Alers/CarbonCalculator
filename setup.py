from setuptools import find_packages, setup

setup(
    name="CarbonCalculator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "black",
        "chardet",
        "ipinfo",
        "keyring",
        "pandas",
        "pre-commit",
        "psutil",
        "pyinstaller",
        "PySide6",
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "pytest-mock",
        "pytest-xvfb",
        "python-dotenv",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "carbon_calculator=main:main",
        ],
    },
)

from setuptools import find_packages, setup

setup(
    name="CarbonCalculator",
    version="0.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5",
        "requests",
        "psutil",
        "pre-commit",
        "black",
        "matplotlib",
        "pyinstaller",
        "python-dotenv",
        "pytest",
        "pytest-mock",
    ],
    entry_points={
        "console_scripts": [
            "carbon_calculator=main:main",
        ],
    },
)

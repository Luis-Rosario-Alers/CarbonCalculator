from setuptools import find_packages, setup

setup(
    name="CarbonCalculator",
    version="0.3.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "psutil",
        "pre-commit",
        "PySide6",
        "qasync",
        "black",
        "Matplotlib",
        "pyinstaller",
        "python-dotenv",
        "pytest",
        "pytest-mock",
        "python-dotenv",
        "aiosqlite",
        "aiofiles",
        "asyncio",
        "aiohttp",
        "pytest-asyncio",
    ],
    entry_points={
        "console_scripts": [
            "carbon_calculator=main:main",
        ],
    },
)

from setuptools import find_packages, setup

setup(
    name="CarbonCalculator",
    version="0.3.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "psutil",
        "pre-commit",
        "PyQt5",
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

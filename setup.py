from setuptools import find_packages, setup

setup(
    name="CarbonCalculator",
    version="0.5.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiofiles",
        "aiohttp",
        "aiosqlite",
        "asyncio",
        "black",
        "chardet",
        "ipinfo",
        "Matplotlib",
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
        "qasync",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "carbon_calculator=main:main",
        ],
    },
)

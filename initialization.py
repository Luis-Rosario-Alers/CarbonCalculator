import os
import platform
import sqlite3
import time
import psutil
import requests

userConsent = False
isNewUser = False


# Checks if the user has an internet connection by attempting to connect to google.com


def main():
    """
    Main function to check internet connection and determine if the user is new.
    """
    checkInternetConnection()
    isNewUserMethod()


def checkInternetConnection():
    """
    Checks if the user has an active internet connection by attempting to connect to google.com.

    Returns:
        bool: True if the internet connection is established, False otherwise.
    """
    url = "https://www.google.com"
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        print("Internet connection is established.")
        return True
    except (requests.ConnectionError, requests.Timeout):
        print("No internet connection. Continuing in offline mode.")
        return False


def isNewUserMethod():
    """
    Determines if the user is new by checking for the existence of the user data database.
    If the database does not exist, it initializes the database.
    """
    global userConsent
    global isNewUser
    if os.path.exists(
        "user_data.db"
    ):  # TODO change this to only look inside of the databases folder
        print("User data found.")
        return False

    else:
        print("User data not found.")
        initDataBase()


def initDataBase():
    """
    Initializes the user data database and collects user consent for data collection.
    If consent is given, it collects device and geographical information and stores it in the database.
    """
    global userConsent
    try:
        if (
            input(
                "Do you consent to data such as device, operating system, or geographical location being collected? (Y/N): "
            ).lower()
            == "y"
        ):
            userConsent = True
        elif (
            input(
                "Do you consent to data such as device information, operating system, or geographical location being collected? (Y/N): "
            ).lower()
            == "n"
        ):
            userConsent = False
            print(
                "You will now be forwarded to the main application.\n please understand that features like saving user data will not be available."
            )
            time.sleep(3)
            # TODO: Add code to forward user to main application
        else:
            raise ValueError("Invalid input. Please try again.")
    except ValueError as e:
        print(e)
    # if user consent is true then we will create the user_data.db file and store the data collected from IPinfo.io and the platform module
    if userConsent:
        device_info = getDeviceInfo()
        location_info = getGeographicalLocation()
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE user_device_info (system TEXT, node TEXT, releaseInfo TEXT, version TEXT, machine TEXT, processor TEXT, cpu_count INTEGER, memory INTEGER)"
        )
        cursor.execute(
            "CREATE TABLE user_geographical_info (ip TEXT, city TEXT, region TEXT, country TEXT, loc TEXT, org TEXT, postal TEXT)"
        )
        conn.commit()
        cursor.execute(
            "INSERT INTO user_device_info (system, node, releaseInfo, version, machine, processor, cpu_count, memory) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                device_info["system"],
                device_info["node"],
                device_info["release"],
                device_info["version"],
                device_info["machine"],
                device_info["processor"],
                device_info["cpu_count"],
                device_info["memory"],
            ),
        )
        cursor.execute(
            "INSERT INTO user_geographical_info (ip, city, region, country, loc, org, postal) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                location_info["ip"],
                location_info["city"],
                location_info["region"],
                location_info["country"],
                location_info["loc"],
                location_info["org"],
                location_info["postal"],
            ),
        )
        conn.commit()
        conn.close()
        print("User data saved.")


def getDeviceInfo():
    """
    Collects and returns device information.

    Returns:
        dict: A dictionary containing device information such as system, node, release, version, machine, processor, CPU count, and memory.
    """
    device_info = {
        "system": platform.system(),  # Operating system name
        "node": platform.node(),  # Hostname
        "release": platform.release(),  # OS release
        "version": platform.version(),  # OS version
        "machine": platform.machine(),  # Machine type
        "processor": platform.processor(),  # Processor type
        "cpu_count": psutil.cpu_count(logical=True),  # Number of logical CPUs
        "memory": psutil.virtual_memory().total,  # Total physical memory
    }
    print("Device information fetched.")
    return device_info


def getGeographicalLocation():
    """
    Fetches and returns geographical location data using the ipinfo.io API.

    Returns:
        dict: A dictionary containing geographical location data such as IP, city, region, country, location, organization, and postal code.
        None: If there is an error fetching the geographical location data.
    """
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        location_info = {
            "ip": data.get("ip"),  # IP address of the user
            "city": data.get("city"),  # City of the user
            "region": data.get("region"),  # Region of the user
            "country": data.get("country"),  # Country of the user
            "loc": data.get("loc"),  # Latitude and longitude of the user
            "org": data.get("org"),  # Organization associated with the IP
            "postal": data.get("postal"),  # Postal code of the user
        }
        print("Geographical location data fetched.")
        return location_info
    except requests.RequestException as e:
        print(f"Error fetching geographical location: {e}")
        return None


main()

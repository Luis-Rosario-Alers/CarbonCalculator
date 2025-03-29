import logging

import ipinfo

logger = logging.getLogger("services")


# EDIT THIS FILE IF YOU NEED TO ALTER THE USER LOCATION DISCOVERY SERVICE


class UserLocationService:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_user_location(self) -> tuple[float, float] | None:
        logger.info("Getting user location")
        handler = ipinfo.getHandler(self.access_token)
        try:
            details = handler.getDetails()
            latitude = details.latitude
            longitude = details.longitude
            logger.info("User location retrieved")

            return latitude, longitude
        except Exception as e:
            logger.error(f"Error fetching user location: {e}")
            return None

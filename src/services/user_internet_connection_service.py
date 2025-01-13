import logging

import aiohttp

logger = logging.getLogger("services")


async def test_user_internet_connection():
    logger.info("Testing internet connection")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.google.com/", timeout=5) as response:
                if response.status == 200:
                    logger.info("Internet connection established.")
                    return True
    except aiohttp.ClientError:
        logger.warning(UserWarning("No internet connection found."))
        logger.info("Program will now proceed in offline mode.")
        logger.info("Note: Some features may not be available.")
        return False

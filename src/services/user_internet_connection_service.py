import logging

import aiohttp

logger = logging.getLogger("services")


async def user_internet_connection_check():
    logger.info("Testing internet connection")
    try:
        async with aiohttp.ClientSession() as session:
            async with await session.get(
                "https://www.google.com/", timeout=5
            ) as response:
                if response.status == 200:
                    logger.info("Internet connection established.")
                    return True
    except aiohttp.ClientError as e:
        logger.error(f"an error occurred testing internet connection: {e}")
        logger.info("Program will now proceed in offline mode.")
        logger.info("Note: Some features may not be available.")
        return False

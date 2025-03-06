import asyncio
import logging

from PySide6.QtWidgets import QWidget

logger = logging.getLogger("Utils")


def connect_async(widget: QWidget, signal: str, async_slot: callable) -> None:
    """
    Connect a Qt widget's signal to an async slot.

    Args:
        widget: The Qt widget that emits the signal
        signal: Name of the signal (e.g., 'clicked')
        async_slot: The async method to call
    """
    loop = asyncio.get_event_loop()

    def signal_wrapper(*args, **kwargs):
        loop.create_task(async_slot(*args, **kwargs))

    connection = getattr(widget, signal).connect(signal_wrapper)
    logger.debug(f"signal connected {connection}")
    return connection

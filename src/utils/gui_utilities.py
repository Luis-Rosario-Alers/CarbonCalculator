import asyncio

from PySide6.QtWidgets import QWidget


def connect_async(widget: QWidget, signal: str, async_slot: callable) -> None:
    """
    Connect a Qt widget's signal to an async slot.

    Args:
        widget: The Qt widget that emits the signal
        signal: Name of the signal (e.g., 'clicked')
        async_slot: The async method to call
    """

    def signal_wrapper(*args, **kwargs):
        asyncio.create_task(async_slot(*args, **kwargs))

    # Get the signal by name and connect wrapper
    getattr(widget, signal).connect(signal_wrapper)

import logging

from PySide6.QtCore import QRunnable, QThreadPool, Slot
from PySide6.QtWidgets import QWidget

logger = logging.getLogger("Utils")


class Worker(QRunnable):
    """
    Worker thread for running tasks in a separate thread.
    """

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self._ref_holder = []

    @Slot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception as e:
            logger.error(f"Error in worker thread: {str(e)} Thread: {self}")


def connect_threaded(widget: QWidget, signal: str, slot: callable) -> None:
    """
    Connect a Qt widget's signal to a slot that will run in a separate thread.

    Args:
        widget: The Qt widget that emits the signal
        signal: Name of the signal (e.g., 'clicked')
        slot: The method to call in a separate thread
    """

    def wrapper(*args, **kwargs):
        # Create a worker and pass the slot function and its arguments
        worker = Worker(slot, *args, **kwargs)

        # Start the thread
        QThreadPool.globalInstance().start(worker)
        logger.debug(f"Worker thread started: {worker}")
        return None

    # Get the signal by name
    qt_signal = getattr(widget, signal)
    logger.debug(f"Qt signal connected: {qt_signal}")
    # Connect the wrapper to the signal
    qt_signal.connect(wrapper)

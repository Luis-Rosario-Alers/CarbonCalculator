import logging

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QWidget

logger = logging.getLogger("Utils")


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    """
    Worker thread for running tasks in a separate thread.
    """

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            logger.error(f"Error in worker thread: {str(e)}")
            self.signals.error.emit((e, type(e), e.__traceback__))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


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
        return None

    # Get the signal by name
    qt_signal = getattr(widget, signal)
    # Connect the wrapper to the signal
    qt_signal.connect(wrapper)

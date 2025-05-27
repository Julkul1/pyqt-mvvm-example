import inspect
import time

from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtProperty

from app.utils.worker import Worker

class TestViewModel(QObject):
    # Signals

    def __init__(self, model):
        # Initialize View Model and Model
        super().__init__()
        self._model = model

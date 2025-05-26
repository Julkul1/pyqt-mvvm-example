import inspect
import time

from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtProperty

from app.utils.worker import Worker

class CounterViewModel(QObject):
    # Signals
    count_changed = pyqtSignal(int)  # Signal to update the count in the views
    can_increment_changed  = pyqtSignal(bool)

    def __init__(self, model):
        # Initialize View Model and Model
        super().__init__()
        self._model = model

    def increment(self):
        self.thread = QThread()

        self.can_increment_changed.emit(False)

        # Assign Background Task to Worker
        self.worker = Worker(self._model.increment)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        # Assign Actions for Worker State Signals
        self.worker.finished.connect(lambda: self.count_changed.emit(self._model.count))
        self.worker.finished.connect(lambda: self.can_increment_changed.emit(True))

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _update_can_increment(self):
        # Example logic: disable button if count >= 10
        new_state = self._model.count < 10
        if new_state != self._can_increment:
            self._can_increment = new_state
            self.can_increment_changed.emit(new_state)
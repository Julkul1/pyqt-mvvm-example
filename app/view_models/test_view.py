from PyQt6.QtCore import QObject


class TestViewModel(QObject):
    # Signals

    def __init__(self, model):
        # Initialize View Model and Model
        super().__init__()
        self._model = model

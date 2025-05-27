import inspect
import time

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from app.view_models.counter_view_model import CounterViewModel
from app.view_models.test_view import TestViewModel
from app.views.counter_view import CounterView
from app.views.main_view import MainView
from app.views.test_view import TestView


class MainViewModel(QObject):
    # Signals
    current_view_changed = pyqtSignal(QWidget)

    def __init__(self, model):
        # Initialize View Model and Model
        super().__init__()
        self._model = model

        self.home_vm = CounterViewModel(self._model)
        self.home_view = CounterView(self.home_vm)

        self.test_vm = TestViewModel(self._model)
        self.test_view = TestView(self.test_vm)


    def set_current_view(self, name):
        if name == "home":
            self.current_view_changed.emit(self.home_view)
        elif name == "settings":
            self.current_view_changed.emit(self.test_view)

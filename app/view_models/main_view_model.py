"""Main view model for the main view."""

from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from app.utils.i18n import set_language
from app.view_models.counter_view_model import CounterViewModel
from app.view_models.test_view_model import TestViewModel
from app.views.counter_view.counter_view import CounterView
from app.views.test_view.test_view import TestView


class MainViewModel(QObject):
    """View model for the main view."""

    current_view_changed = pyqtSignal(QWidget)
    language_changed = pyqtSignal(str)
    _model: Any
    home_vm: CounterViewModel
    home_view: CounterView
    test_vm: TestViewModel
    test_view: TestView

    def __init__(self, model: Any) -> None:
        """Initialize the main view model.

        Args:
            model: The main model.
        """
        super().__init__()
        self._model = model

        self.home_vm = CounterViewModel(self._model)
        self.home_view = CounterView(self.home_vm)

        self.test_vm = TestViewModel(self._model)
        self.test_view = TestView(self._model)

    def set_current_view(self, name: str) -> None:
        """Set the current view based on the given name.

        Args:
            name (str): The name of the view to display.
        """
        if name == "home":
            self.current_view_changed.emit(self.home_view)
        elif name == "settings":
            self.current_view_changed.emit(self.test_view)

    def set_language(self, language_code: str) -> None:
        """Set the application language.

        Args:
            language_code (str): The language code to set.
        """
        set_language(language_code)
        self.language_changed.emit(language_code)

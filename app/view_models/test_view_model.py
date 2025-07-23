"""Test view model for demonstration purposes."""

from typing import Any

from PyQt6.QtCore import QObject


class TestViewModel(QObject):
    """A simple test view model for demonstration purposes."""

    model: Any

    def __init__(self, model: Any) -> None:
        """Initialize the test view model.

        Args:
            model: The model for the test view.
        """
        super().__init__()
        self.model = model

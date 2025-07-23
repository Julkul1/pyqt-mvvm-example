"""Test view model for demonstration purposes."""

from PyQt6.QtCore import QObject


class TestViewModel(QObject):
    """A simple test view model for demonstration purposes."""

    def __init__(self, model):
        """Initialize the test view model.

        Args:
            model: The model for the test view.
        """
        super().__init__()
        self.model = model

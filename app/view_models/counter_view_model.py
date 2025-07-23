"""Counter view model for the counter view."""

from PyQt6.QtCore import QObject, pyqtSignal


class CounterViewModel(QObject):
    """View model for the counter view."""

    count_changed = pyqtSignal(int)  # Signal to update the count in the views
    can_increment_changed = pyqtSignal(bool)

    def __init__(self, model):
        """Initialize the counter view model.

        Args:
            model: The counter model.
        """
        super().__init__()
        self.model = model

    def increment(self):
        """Increment the counter in the model."""
        self.model.increment()

"""Counter view for displaying and interacting with the counter."""

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class CounterView(QWidget):
    """View for displaying and interacting with the counter."""

    def __init__(self, view_model):
        """Initialize the counter view.

        Args:
            view_model: The view model for the counter.
        """
        super().__init__()
        self.view_model = view_model
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components for the counter view."""
        self.layout = QVBoxLayout()
        self.label = QLabel("0")
        self.button = QPushButton("Increment")
        self.button.clicked.connect(self.view_model.increment)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def update_label(self, count):
        """Update the label to show the current count.

        Args:
            count (int): The current count value.
        """
        self.label.setText(str(count))

    def update_button(self, is_enabled):
        """Enable or disable the increment button.

        Args:
            is_enabled (bool): Whether the button should be enabled.
        """
        self.button.setEnabled(is_enabled)

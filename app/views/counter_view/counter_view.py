"""Counter view for displaying and interacting with the counter."""

from typing import Any

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class CounterView(QWidget):
    """View for displaying and interacting with the counter."""

    view_model: Any
    layout_: QVBoxLayout
    label: QLabel
    button: QPushButton

    def __init__(self, view_model: Any) -> None:
        """Initialize the counter view.

        Args:
            view_model: The view model for the counter.
        """
        super().__init__()
        self.view_model = view_model
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components for the counter view."""
        self.layout_ = QVBoxLayout()
        self.label = QLabel("0")
        self.button = QPushButton("Increment")
        self.button.clicked.connect(self.view_model.increment)
        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.button)
        self.setLayout(self.layout_)

    def update_label(self, count: int) -> None:
        """Update the label to show the current count.

        Args:
            count (int): The current count value.
        """
        self.label.setText(str(count))

    def update_button(self, is_enabled: bool) -> None:
        """Enable or disable the increment button.

        Args:
            is_enabled (bool): Whether the button should be enabled.
        """
        self.button.setEnabled(is_enabled)

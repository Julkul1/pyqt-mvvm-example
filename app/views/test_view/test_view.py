"""Test view for demonstration purposes."""

from typing import Any

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class TestView(QWidget):
    """A simple test view for demonstration purposes."""

    view_model: Any

    def __init__(self, view_model: Any) -> None:
        """Initialize the test view.

        Args:
            view_model: The view model for the test view.
        """
        super().__init__()
        self.view_model = view_model
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components for the test view."""
        layout = QHBoxLayout()
        label = QLabel("Test View")
        layout.addWidget(label)
        self.setLayout(layout)

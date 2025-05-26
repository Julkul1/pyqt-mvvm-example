from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from app.utils.utils import load_stylesheet


class CounterView(QWidget):
    def __init__(self, view_model):
        # Initialize View and View Model
        super().__init__()
        self._view_model = view_model

        # Initialize Stylesheet
        self.stylesheet = load_stylesheet("counter_view.qss")

        # Connect Signals to Slots
        self._view_model.count_changed.connect(self.update_label)
        self._view_model.can_increment_changed.connect(self.update_button)

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        # Set Layout
        self.layout = QVBoxLayout()  # Vertical layout
        self.setLayout(self.layout)

        # Create Widgets
        self.label = QLabel('0')  # Label to show the count
        self.button = QPushButton('Increment')  # Button to increment the count

        # Bind Commands
        self.button.clicked.connect(self._view_model.increment)  # Connect button click to ViewModel

        # Set Style
        self.button.setStyleSheet(self.stylesheet)

        # Add Widgets to View
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

    def update_label(self, count):
        self.label.setText(str(count))  # Update the label with the current count

    def update_button(self, is_enabled):
        self.button.setEnabled(is_enabled)
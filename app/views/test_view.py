from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget


class TestView(QWidget):
    def __init__(self, view_model):
        # Initialize View and View Model
        super().__init__()
        self._view_model = view_model

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        # Set Layout
        self.main_layout = QHBoxLayout()  # Vertical layout
        self.setLayout(self.main_layout)

        # Create Widgets
        self.label = QLabel("Bruh")

        # Add Widgets to View
        self.main_layout.addWidget(self.label)

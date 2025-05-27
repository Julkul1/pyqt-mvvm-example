from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget

from app.utils.utils import load_stylesheet


class MainView(QWidget):
    def __init__(self, view_model):
        # Initialize View and View Model
        super().__init__()
        self._view_model = view_model

        # Initialize Stylesheet

        # Connect Signals to Slots
        self._view_model.current_view_changed.connect(self.change_view)

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        # Set Layout
        self.main_layout = QVBoxLayout()  # Vertical layout
        self.setLayout(self.main_layout)

        # Create Widgets
        navbar_layout = self.init_navbar()
        self.stacked_widget = QStackedWidget()

        # Bind Commands

        # Set Style

        # Add Widgets to View
        self.main_layout.addWidget(navbar_layout)
        self.main_layout.addWidget(self.stacked_widget)

    def init_navbar(self):
        # Set Layout
        navbar_layout = QHBoxLayout()

        # Create Widgets
        self.button_home = QPushButton("Home")
        self.button_settings = QPushButton("Settings")

        # Bind Commands
        self.button_home.clicked.connect(lambda: self._view_model.set_current_view("home"))
        self.button_settings.clicked.connect(lambda: self._view_model.set_current_view("settings"))

        # Add Widgets to Layout
        navbar_layout.addWidget(self.button_home)
        navbar_layout.addWidget(self.button_settings)
        navbar_layout.addStretch()

        # Encapsulate in QWidget
        navbar_widget = QWidget()
        navbar_widget.setLayout(navbar_layout)
        navbar_widget.setFixedHeight(100)
        navbar_widget.setStyleSheet("""
            background-color: #f0f0f0;  /* optional background */
            border-bottom: 2px solid #cccccc;  /* bottom border only */
        """)

        return navbar_widget

    def change_view(self, widget: QWidget):
        index = self.stacked_widget.indexOf(widget)
        if index == -1:
            self.stacked_widget.addWidget(widget)
            index = self.stacked_widget.indexOf(widget)
        self.stacked_widget.setCurrentIndex(index)
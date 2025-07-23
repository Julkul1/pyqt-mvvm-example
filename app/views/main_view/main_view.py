"""Main view for the application UI."""

from typing import Any

from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.utils.i18n import use_translate


class MainView(QWidget):
    """Main view for the application UI."""

    _view_model: Any
    t: Any
    main_layout: QVBoxLayout
    stacked_widget: QStackedWidget
    button_home: QPushButton
    button_settings: QPushButton
    language_selector: QComboBox

    def __init__(self, view_model: Any) -> None:
        """Initialize the main view.

        Args:
            view_model: The main view model.
        """
        super().__init__()
        self._view_model = view_model
        self.t = use_translate()

        # Connect Signals to Slots
        self._view_model.current_view_changed.connect(self.change_view)
        if hasattr(self._view_model, "language_changed"):
            self._view_model.language_changed.connect(self.update_translations)

        # Initialize the UI
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components for the main view."""
        self.main_layout = QVBoxLayout()  # Vertical layout
        self.setLayout(self.main_layout)

        # Create Widgets
        navbar_layout = self.init_navbar()
        self.stacked_widget = QStackedWidget()

        # Add Widgets to View
        self.main_layout.addWidget(navbar_layout)
        self.main_layout.addWidget(self.stacked_widget)

    def init_navbar(self) -> QWidget:
        """Initialize the navigation bar for the main view.

        Returns:
            QWidget: The navigation bar widget.
        """
        navbar_layout = QHBoxLayout()

        # Create Widgets
        self.button_home = QPushButton(self.t("Home"))
        self.button_settings = QPushButton(self.t("Settings"))

        # Language selector
        self.language_selector = QComboBox()
        # Example: populate with available languages
        import os

        locales_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets",
            "locales",
        )
        langs = []
        if os.path.exists(locales_path):
            langs = [
                d
                for d in os.listdir(locales_path)
                if os.path.isdir(os.path.join(locales_path, d))
            ]
        if langs:
            self.language_selector.addItems(langs)
        else:
            self.language_selector.addItems(["en", "pl"])
        self.language_selector.currentTextChanged.connect(self._view_model.set_language)

        # Bind Commands
        self.button_home.clicked.connect(
            lambda: self._view_model.set_current_view("home")
        )
        self.button_settings.clicked.connect(
            lambda: self._view_model.set_current_view("settings")
        )
        self.button_home.setStyleSheet("""
            background-color: #00FF00;  /* optional background */
            border-bottom: 2px solid #cccccc;  /* bottom border only */
        """)

        # Add Widgets to Layout
        navbar_layout.addWidget(self.button_home)
        navbar_layout.addWidget(self.button_settings)
        navbar_layout.addStretch()
        navbar_layout.addWidget(self.language_selector)

        # Encapsulate in QWidget
        navbar_widget = QWidget()
        navbar_widget.setLayout(navbar_layout)
        navbar_widget.setFixedHeight(100)
        navbar_widget.setStyleSheet("""
            background-color: #F0F0F0;  /* optional background */
            border-bottom: 2px solid #cccccc;  /* bottom border only */
        """)

        return navbar_widget

    def change_view(self, widget: QWidget) -> None:
        """Change the current view in the stacked widget.

        Args:
            widget (QWidget): The widget to display.
        """
        index = self.stacked_widget.indexOf(widget)
        if index == -1:
            self.stacked_widget.addWidget(widget)
            index = self.stacked_widget.indexOf(widget)
        self.stacked_widget.setCurrentIndex(index)

    def update_translations(self, language_code: str) -> None:
        """Update UI text when language changes.

        Args:
            language_code (str): The new language code.
        """
        self.button_home.setText(self.t("Home"))
        self.button_settings.setText(self.t("Settings"))

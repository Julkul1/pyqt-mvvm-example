"""Main application window module."""

import os

from PyQt6.QtWidgets import QMainWindow

from app.models.counter_model import CounterModel
from app.utils.config import AppConfig
from app.utils.i18n import init_i18n
from app.view_models.main_view_model import MainViewModel
from app.views.main_view import MainView


class MainWindow(QMainWindow):
    """Main application window for the PyQt app."""

    def __init__(self) -> None:
        """Initialize the Main-Window."""
        super().__init__()
        # Window-Settings
        self.setWindowTitle(AppConfig.app_name())
        self.resize(AppConfig.window_width(), AppConfig.window_height())

        model = CounterModel()
        # Setup global i18n
        locales_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "locales"
        )
        init_i18n(locales_path, default_language="en")
        view_model = MainViewModel(model)
        view = MainView(view_model)
        self.setCentralWidget(view)
        view.show()

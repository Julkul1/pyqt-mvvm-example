import sys
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.models.counter_model import CounterModel
from app.utils.config import AppConfig
from app.views.counter_view import CounterView
from app.view_models.counter_view_model import CounterViewModel


def run() -> int:
    """
    Initializes the application and runs it.

    Returns:
        int: The exit status code.
    """
    app: QApplication = QApplication(sys.argv)
    AppConfig.initialize()

    window: MainWindow = MainWindow()
    window.show()
    return sys.exit(app.exec())
from PyQt6.QtWidgets import QMainWindow

from app.models.counter_model import CounterModel
from app.utils.config import AppConfig
from app.view_models.main_view_model import MainViewModel
from app.views.main_view import MainView


class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow (QMainWindow): Inheritance
    """

    def __init__(self) -> None:
        """
        Initialize the Main-Window.
        """
        super().__init__()
        # Window-Settings
        self.setWindowTitle(AppConfig.app_name())
        self.resize(AppConfig.window_width(), AppConfig.window_height())

        model = CounterModel()
        view_model = MainViewModel(model)
        view = MainView(view_model)
        self.setCentralWidget(view)
        view.show()

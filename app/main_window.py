from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from app.models.counter_model import CounterModel
from app.utils.config import AppConfig
from app.views.counter_view import CounterView
from app.view_models.counter_view_model import CounterViewModel


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
        view_model = CounterViewModel(model)
        view = CounterView(view_model)
        self.setCentralWidget(view)
        view.show()
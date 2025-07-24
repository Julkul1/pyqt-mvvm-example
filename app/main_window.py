from PyQt6.QtWidgets import QMainWindow

from app.app_context import AppContext
from app.models.counter_model import CounterModel
from app.utils.paths import local_path
from app.view_models.main_view_model import MainViewModel
from app.views.main_view.main_view import MainView


class MainWindow(QMainWindow):
    """Main application window for the PyQt app."""

    def __init__(self, context: AppContext) -> None:
        """Initialize the Main-Window.

        Args:
            context (AppContext): The application context.
        """
        super().__init__()
        self.context = context
        # Window-Settings
        self.setWindowTitle(self.context.config.app_name())
        self.resize(
            self.context.config.window_width(), self.context.config.window_height()
        )

        model = CounterModel()
        view_model = MainViewModel(model)
        view = MainView(view_model)
        self.setCentralWidget(view)
        view.show()

        # Theme support
        self.context.theme_manager.theme_changed.connect(self.reload_stylesheet)
        self.reload_stylesheet()

    def reload_stylesheet(self) -> None:
        """Reload the stylesheet for the main window."""
        qss_path = local_path(__file__, "stylesheet.qss")
        qss = self.context.theme_manager.load_stylesheet_with_theme(str(qss_path))
        self.setStyleSheet(qss)

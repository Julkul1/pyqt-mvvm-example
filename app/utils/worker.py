"""Worker utilities for running functions in background threads."""

from PyQt6.QtCore import QObject


class Worker(QObject):
    """General-purpose worker for running any function in a background thread."""

    def __init__(self, fn, *args, **kwargs):
        """Initialize the worker.

        Args:
            fn: The function to run.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Run the worker function in a background thread."""
        self.fn(*self.args, **self.kwargs)

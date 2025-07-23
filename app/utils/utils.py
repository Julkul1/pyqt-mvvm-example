"""Utility functions for the application."""

import os
import sys


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_stylesheet(filename: str) -> str:
    """Load a QSS stylesheet from a file.

    Args:
        filename (str): The path to the QSS file.

    Returns:
        str: The contents of the stylesheet.
    """
    with open(filename, "r") as f:
        return f.read()

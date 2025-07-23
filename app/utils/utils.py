import sys
from pathlib import Path


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(relative_path)


def load_stylesheet(filename: str) -> str:
    stylesheet_path = resource_path(f"app/views/{filename}")
    return stylesheet_path.read_text()

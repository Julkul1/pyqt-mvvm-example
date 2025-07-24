from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# App root
APP_DIR = PROJECT_ROOT / "app"

# Assets and subdirectories
ASSETS_DIR = PROJECT_ROOT / "assets"
THEMES_DIR = ASSETS_DIR / "themes"
LOCALES_DIR = ASSETS_DIR / "locales"
FONTS_DIR = ASSETS_DIR / "fonts"
IMAGES_DIR = ASSETS_DIR / "images"

# App subdirectories
UTILS_DIR = APP_DIR / "utils"
VIEWS_DIR = APP_DIR / "views"
VIEW_MODELS_DIR = APP_DIR / "view_models"
MODELS_DIR = APP_DIR / "models"

# Config and other important files
CONFIG_PATH = PROJECT_ROOT / "config.ini"
PYPROJECT_TOML = PROJECT_ROOT / "pyproject.toml"
REQUIREMENTS_TXT = PROJECT_ROOT / "requirements.txt"


def local_path(module_file: str, *parts: str) -> Path:
    """Return a path relative to the directory of the given module file.

    Args:
        module_file (str): The __file__ of the calling module.
        *parts (str): Path components relative to the module's directory.

    Returns:
        Path: The absolute path resolved from the module's directory and parts.
    """
    return Path(module_file).parent.joinpath(*parts)


# Example usage:
# from app.utils.paths import THEMES_DIR, CONFIG_PATH
# theme_path = THEMES_DIR / "dark.json"

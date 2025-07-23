"""i18n utilities for translation management."""

from typing import Callable, Optional

from app.utils.i18n_manager import I18nManager

_manager: Optional[I18nManager] = None


def init_i18n(locales_path: str, default_language: str = "en") -> None:
    """Initialize the global I18nManager.

    Args:
        locales_path (str): Path to the locales directory.
        default_language (str): The default language code.
    """
    global _manager
    _manager = I18nManager(locales_path, default_language)


def set_language(language_code: str) -> None:
    """Set the current language for translations.

    Args:
        language_code (str): The language code to set.
    """
    if _manager:
        _manager.load_language(language_code)


def use_translate() -> Callable[[str], str]:
    """Get the translation function for the current language.

    Returns:
        Callable[[str], str]: The translation function.
    """
    if _manager:
        return _manager.t
    return lambda key: key


def get_manager() -> Optional[I18nManager]:
    """Get the current I18nManager instance.

    Returns:
        I18nManager: The current manager instance.
    """
    return _manager

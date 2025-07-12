"""
Translation Manager

This module provides a global translation manager that can be used
throughout the application for easy access to translations.
"""

from typing import Optional
from functools import lru_cache
from .translation_service import TranslationService


class TranslationManager:
    """Global translation manager singleton"""
    
    _instance: Optional['TranslationManager'] = None
    _service: Optional[TranslationService] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._service = TranslationService()
            self._initialized = True
    
    @property
    def service(self) -> TranslationService:
        """Get the translation service"""
        return self._service
    
    def tr(self, key: str, default: Optional[str] = None) -> str:
        """Translate a key (shortcut method)"""
        return self._service.translate(key, default)
    
    def tr_plural(self, key: str, count: int, default: Optional[str] = None) -> str:
        """Translate with plural forms (shortcut method)"""
        return self._service.translate_plural(key, count, default)
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        return self._service.set_language(language_code)
    
    def get_current_language(self) -> str:
        """Get current language"""
        return self._service.get_current_language()
    
    def get_available_languages(self) -> list[str]:
        """Get available languages"""
        return self._service.get_available_languages()


# Global instance
_translation_manager = TranslationManager()


def tr(key: str, default: Optional[str] = None) -> str:
    """Global translation function"""
    return _translation_manager.tr(key, default)


def tr_plural(key: str, count: int, default: Optional[str] = None) -> str:
    """Global plural translation function"""
    return _translation_manager.tr_plural(key, count, default)


def set_language(language_code: str) -> bool:
    """Set the current language globally"""
    return _translation_manager.set_language(language_code)


def get_current_language() -> str:
    """Get current language globally"""
    return _translation_manager.get_current_language()


def get_available_languages() -> list[str]:
    """Get available languages globally"""
    return _translation_manager.get_available_languages()


def get_translation_manager() -> TranslationManager:
    """Get the global translation manager instance"""
    return _translation_manager


# Convenience functions for common translation patterns
@lru_cache(maxsize=128)
def tr_ui(key: str, default: Optional[str] = None) -> str:
    """Translate UI elements with caching"""
    return tr(f"ui.{key}", default)


@lru_cache(maxsize=128)
def tr_msg(key: str, default: Optional[str] = None) -> str:
    """Translate messages with caching"""
    return tr(f"messages.{key}", default)


@lru_cache(maxsize=128)
def tr_error(key: str, default: Optional[str] = None) -> str:
    """Translate error messages with caching"""
    return tr(f"errors.{key}", default)


@lru_cache(maxsize=128)
def tr_dialog(key: str, default: Optional[str] = None) -> str:
    """Translate dialog elements with caching"""
    return tr(f"dialogs.{key}", default)


@lru_cache(maxsize=128)
def tr_common(key: str, default: Optional[str] = None) -> str:
    """Translate common elements with caching"""
    return tr(f"common.{key}", default) 
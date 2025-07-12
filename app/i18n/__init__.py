# Internationalization (i18n) package for translations

from .translation_manager import (
    tr, tr_plural, set_language, get_current_language,
    get_available_languages, get_translation_manager
)

__all__ = [
    'tr',
    'tr_plural', 
    'set_language',
    'get_current_language',
    'get_available_languages',
    'get_translation_manager'
] 
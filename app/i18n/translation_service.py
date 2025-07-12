"""
Translation Service Implementation

This service provides internationalization support for the application,
implementing the core translation interface.
"""

import os
import json
from typing import Dict, Optional, List
from pathlib import Path
from PyQt6.QtCore import QTranslator, QCoreApplication, QLocale
from PyQt6.QtWidgets import QApplication

from app.core.interfaces import TranslationServiceInterface


class TranslationService(TranslationServiceInterface):
    """Translation service implementation for PyQt applications"""
    
    def __init__(self, translations_dir: str = "translations"):
        self.translations_dir = Path(translations_dir)
        self.current_language = "en"
        self.fallback_language = "en"
        self.translations: Dict[str, Dict[str, str]] = {}
        self.qt_translator = QTranslator()
        
        # Ensure translations directory exists
        self.translations_dir.mkdir(exist_ok=True)
        
        # Load available languages
        self.available_languages = self._discover_languages()
        
        # Load translations
        self._load_translations()
    
    def _discover_languages(self) -> List[str]:
        """Discover available language files"""
        languages = []
        if self.translations_dir.exists():
            for file_path in self.translations_dir.glob("*.json"):
                lang_code = file_path.stem
                languages.append(lang_code)
        return languages
    
    def _load_translations(self) -> None:
        """Load all translation files"""
        for lang_code in self.available_languages:
            file_path = self.translations_dir / f"{lang_code}.json"
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading translations for {lang_code}: {e}")
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        return self.available_languages.copy()
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code not in self.available_languages:
            print(f"Language {language_code} not available")
            return False
        
        self.current_language = language_code
        
        # Update Qt translator
        app = QApplication.instance()
        if app:
            app.removeTranslator(self.qt_translator)
            if language_code != "en":  # English is default
                qt_file = self.translations_dir / f"{language_code}.qm"
                if qt_file.exists():
                    self.qt_translator.load(str(qt_file))
                    app.installTranslator(self.qt_translator)
        
        return True
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """Translate a key to the current language"""
        if not key:
            return default or ""
        
        # Try current language
        if (self.current_language in self.translations and 
            key in self.translations[self.current_language]):
            return self.translations[self.current_language][key]
        
        # Try fallback language
        if (self.fallback_language in self.translations and 
            key in self.translations[self.fallback_language]):
            return self.translations[self.fallback_language][key]
        
        # Return default or key
        return default or key
    
    def translate_plural(self, key: str, count: int, default: Optional[str] = None) -> str:
        """Translate with plural forms support"""
        if count == 1:
            # Singular form
            singular_key = f"{key}_singular"
            return self.translate(singular_key, default or key)
        else:
            # Plural form
            plural_key = f"{key}_plural"
            return self.translate(plural_key, default or key)
    
    def get_language_name(self, language_code: str) -> str:
        """Get the display name of a language"""
        language_names = {
            "en": "English",
            "pl": "Polski"
        }
        return language_names.get(language_code, language_code)
    
    def get_system_language(self) -> str:
        """Get the system language code"""
        locale = QLocale.system()
        language_code = locale.name().split('_')[0]
        
        # Map to supported languages
        if language_code in self.available_languages:
            return language_code
        elif language_code.startswith('pl'):
            return "pl"
        else:
            return "en"
    
    def reload_translations(self) -> None:
        """Reload all translation files"""
        self.translations.clear()
        self.available_languages = self._discover_languages()
        self._load_translations()
    
    def add_translation(self, language_code: str, key: str, value: str) -> None:
        """Add a single translation"""
        if language_code not in self.translations:
            self.translations[language_code] = {}
        
        self.translations[language_code][key] = value
    
    def save_translations(self, language_code: str) -> bool:
        """Save translations for a language to file"""
        if language_code not in self.translations:
            return False
        
        file_path = self.translations_dir / f"{language_code}.json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.translations[language_code], f, 
                         ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving translations for {language_code}: {e}")
            return False 
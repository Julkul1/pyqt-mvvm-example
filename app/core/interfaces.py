"""
Core interfaces for the application

This module defines the core interfaces that establish contracts
between different layers of the application.
"""

from typing import Protocol, Dict, List, Optional, Any
from abc import ABC, abstractmethod


class LoggerServiceInterface(Protocol):
    """Interface for logging services"""
    
    def debug(self, message: str) -> None:
        """Log a debug message"""
        ...
    
    def info(self, message: str) -> None:
        """Log an info message"""
        ...
    
    def warning(self, message: str) -> None:
        """Log a warning message"""
        ...
    
    def error(self, message: str) -> None:
        """Log an error message"""
        ...
    
    def critical(self, message: str) -> None:
        """Log a critical message"""
        ...


class ConfigurationServiceInterface(Protocol):
    """Interface for configuration services"""
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        ...
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        ...
    
    def has(self, key: str) -> bool:
        """Check if a configuration key exists"""
        ...
    
    def delete(self, key: str) -> None:
        """Delete a configuration key"""
        ...
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        ...
    
    def save(self) -> bool:
        """Save configuration to storage"""
        ...
    
    def load(self) -> bool:
        """Load configuration from storage"""
        ...


class DataServiceInterface(Protocol):
    """Interface for data services"""
    
    def save_data(self, key: str, data: Any) -> bool:
        """Save data with a key"""
        ...
    
    def load_data(self, key: str, default: Any = None) -> Any:
        """Load data by key"""
        ...
    
    def delete_data(self, key: str) -> bool:
        """Delete data by key"""
        ...
    
    def has_data(self, key: str) -> bool:
        """Check if data exists for a key"""
        ...
    
    def list_keys(self) -> List[str]:
        """List all available data keys"""
        ...
    
    def clear_all(self) -> bool:
        """Clear all data"""
        ...


class TranslationServiceInterface(Protocol):
    """Interface for translation services"""
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages"""
        ...
    
    def get_current_language(self) -> str:
        """Get current language code"""
        ...
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        ...
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """Translate a key to the current language"""
        ...
    
    def translate_plural(self, key: str, count: int, default: Optional[str] = None) -> str:
        """Translate with plural forms support"""
        ...
    
    def get_language_name(self, language_code: str) -> str:
        """Get the display name of a language"""
        ...
    
    def get_system_language(self) -> str:
        """Get the system language code"""
        ...
    
    def reload_translations(self) -> None:
        """Reload all translation files"""
        ...
    
    def add_translation(self, language_code: str, key: str, value: str) -> None:
        """Add a single translation"""
        ...
    
    def save_translations(self, language_code: str) -> bool:
        """Save translations for a language to file"""
        ... 
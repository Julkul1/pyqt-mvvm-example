"""
Application initialization module

This module handles the initialization of the application,
including services, configuration, and global setup.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale

from app.services.console_logger_service import ConsoleLoggerService
from app.services.local_config_service import LocalConfigService
from app.services.local_data_service import LocalDataService
from app.services.fuzzy_logic_service import FuzzyLogicService
from app.services.theme_service import ThemeService
from app.utils.thread_manager import ThreadManager
from app.i18n.translation_manager import get_translation_manager, set_language


class ApplicationInitializer:
    """Handles application initialization"""
    
    def __init__(self):
        self.app = None
        self.logger = None
        self.config_service = None
        self.data_service = None
        self.fuzzy_logic_service = None
        self.theme_service = None
        self.thread_manager = None
        self.translation_manager = None
    
    def initialize(self, app: QApplication) -> bool:
        """Initialize the application"""
        try:
            self.app = app
            
            # Initialize services
            self._initialize_services()
            
            # Initialize i18n
            self._initialize_i18n()
            
            # Initialize theme
            self._initialize_theme()
            
            # Log successful initialization
            self.logger.info("Application initialized successfully")
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize application: {e}")
            return False
    
    def _initialize_services(self):
        """Initialize all application services"""
        # Initialize logger first
        self.logger = ConsoleLoggerService()
        self.logger.info("Initializing application services...")
        
        # Initialize configuration service
        self.config_service = LocalConfigService()
        self.config_service.load()
        self.logger.info("Configuration service initialized")
        
        # Initialize data service
        self.data_service = LocalDataService()
        self.logger.info("Data service initialized")
        
        # Initialize fuzzy logic service
        self.fuzzy_logic_service = FuzzyLogicService()
        self.logger.info("Fuzzy logic service initialized")
        
        # Initialize theme service
        self.theme_service = ThemeService()
        self.logger.info("Theme service initialized")
        
        # Initialize thread manager
        self.thread_manager = ThreadManager()
        self.logger.info("Thread manager initialized")
    
    def _initialize_i18n(self):
        """Initialize internationalization"""
        try:
            # Get translation manager
            self.translation_manager = get_translation_manager()
            
            # Get system language or default to English
            system_lang = self.translation_manager.service.get_system_language()
            available_langs = self.translation_manager.get_available_languages()
            
            # Set language based on system or configuration
            config_lang = self.config_service.get("language", None)
            if config_lang and config_lang in available_langs:
                target_lang = config_lang
            elif system_lang in available_langs:
                target_lang = system_lang
            else:
                target_lang = "en"  # Default to English
            
            # Set the language
            success = set_language(target_lang)
            if success:
                self.logger.info(f"Language set to: {target_lang}")
            else:
                self.logger.warning(f"Failed to set language to {target_lang}, using English")
                set_language("en")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize i18n: {e}")
            # Fallback to English
            set_language("en")
    
    def _initialize_theme(self):
        """Initialize theme system"""
        try:
            # Get theme from configuration or use default
            theme_name = self.config_service.get("theme", "default")
            
            # Apply theme
            success = self.theme_service.apply_theme(theme_name)
            if success:
                self.logger.info(f"Theme applied: {theme_name}")
            else:
                self.logger.warning(f"Failed to apply theme {theme_name}, using default")
                self.theme_service.apply_theme("default")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize theme: {e}")
            # Apply default theme
            self.theme_service.apply_theme("default")
    
    def get_services(self):
        """Get all initialized services"""
        return {
            'logger': self.logger,
            'config': self.config_service,
            'data': self.data_service,
            'fuzzy_logic': self.fuzzy_logic_service,
            'theme': self.theme_service,
            'thread_manager': self.thread_manager,
            'translation': self.translation_manager
        }
    
    def cleanup(self):
        """Cleanup resources before application exit"""
        try:
            if self.logger:
                self.logger.info("Cleaning up application resources...")
            
            # Save configuration
            if self.config_service:
                self.config_service.save()
            
            # Stop all threads
            if self.thread_manager:
                self.thread_manager.stop_all_tasks()
            
            if self.logger:
                self.logger.info("Application cleanup completed")
                
        except Exception as e:
            print(f"Error during cleanup: {e}")


# Global initializer instance
_initializer = ApplicationInitializer()


def initialize_app(app: QApplication) -> bool:
    """Initialize the application"""
    return _initializer.initialize(app)


def get_services():
    """Get all application services"""
    return _initializer.get_services()


def cleanup_app():
    """Cleanup application resources"""
    _initializer.cleanup()
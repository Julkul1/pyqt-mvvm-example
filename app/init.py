"""
Application initialization for Fuzzy Logic Editor
"""

from app.services.logger_service import LoggerService
from app.services.configuration_service import ConfigurationService
from app.services.data_service import DataService


def initialize_application():
    """Initialize the application and create services"""
    # Create logger for initialization
    logger = LoggerService()
    logger.info("Fuzzy Logic Editor initialization started")
    
    # Initialize configuration
    config_service = ConfigurationService(logger)
    logger.info("Configuration service initialized")
    
    # Initialize data service
    data_service = DataService(logger)
    logger.info("Data service initialized")
    
    logger.info("Fuzzy Logic Editor initialization completed")
    
    return logger, config_service, data_service


def run():
    """Legacy run function for backward compatibility"""
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    initialize_application()
    
    from app.main_window import MainWindow
    window = MainWindow()
    window.show()
    
    return app.exec()
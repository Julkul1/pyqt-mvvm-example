#!/usr/bin/env python3
"""
Fuzzy Logic Editor - Main Application Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.init import initialize_application
from app.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Initialize application
    initialize_application()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
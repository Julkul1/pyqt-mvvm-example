"""
Example usage of the i18n translation system

This module demonstrates how to use the internationalization
system in the PyQt MVVM application.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import Qt

from app.i18n.translation_manager import tr, tr_plural, set_language, get_available_languages
from app.i18n.language_selector import LanguageSelector, CompactLanguageSelector


class ExampleWindow(QMainWindow):
    """Example window demonstrating i18n usage"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.update_texts()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle(tr("app.title", "PyQt MVVM Example"))
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Title label
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.title_label)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Buttons
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.on_add_clicked)
        layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton()
        self.edit_button.clicked.connect(self.on_edit_clicked)
        layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton()
        self.delete_button.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.delete_button)
        
        # Language selector
        self.language_selector = LanguageSelector()
        self.language_selector.language_changed.connect(self.on_language_changed)
        layout.addWidget(self.language_selector)
        
        # Compact language selector
        self.compact_selector = CompactLanguageSelector()
        self.compact_selector.language_changed.connect(self.on_language_changed)
        layout.addWidget(self.compact_selector)
        
        # Language info
        self.language_info = QLabel()
        layout.addWidget(self.language_info)
        
        layout.addStretch()
    
    def update_texts(self):
        """Update all text elements with current translations"""
        # Update window title
        self.setWindowTitle(tr("app.title", "PyQt MVVM Example"))
        
        # Update labels
        self.title_label.setText(tr("main_window.title", "Fuzzy Logic System"))
        self.status_label.setText(tr("main_window.status.ready", "Ready"))
        
        # Update buttons
        self.add_button.setText(tr("fuzzy_sets.add_set", "Add Fuzzy Set"))
        self.edit_button.setText(tr("fuzzy_sets.edit_set", "Edit Fuzzy Set"))
        self.delete_button.setText(tr("fuzzy_sets.delete_set", "Delete Fuzzy Set"))
        
        # Update language info
        current_lang = tr("languages.language", "Language")
        available_langs = get_available_languages()
        self.language_info.setText(f"{current_lang}: {', '.join(available_langs)}")
    
    def on_add_clicked(self):
        """Handle add button click"""
        print(tr("messages.info", "Info") + ": " + tr("fuzzy_sets.add_set", "Add Fuzzy Set"))
    
    def on_edit_clicked(self):
        """Handle edit button click"""
        print(tr("messages.info", "Info") + ": " + tr("fuzzy_sets.edit_set", "Edit Fuzzy Set"))
    
    def on_delete_clicked(self):
        """Handle delete button click"""
        print(tr("messages.warning", "Warning") + ": " + tr("messages.confirm_delete", "Are you sure?"))
    
    def on_language_changed(self, language_code: str):
        """Handle language change"""
        print(f"Language changed to: {language_code}")
        self.update_texts()


def demonstrate_basic_usage():
    """Demonstrate basic translation usage"""
    print("=== Basic Translation Usage ===")
    
    # Set language
    set_language("en")
    print(f"English: {tr('app.title')}")
    print(f"English: {tr('main_window.status.ready')}")
    
    set_language("pl")
    print(f"Polish: {tr('app.title')}")
    print(f"Polish: {tr('main_window.status.ready')}")
    
    # Test missing translation
    print(f"Missing key: {tr('nonexistent.key', 'Default Text')}")


def demonstrate_plural_forms():
    """Demonstrate plural forms support"""
    print("\n=== Plural Forms ===")
    
    set_language("en")
    print(f"1 item: {tr_plural('items', 1, '1 item')}")
    print(f"5 items: {tr_plural('items', 5, '5 items')}")
    
    set_language("pl")
    print(f"1 element: {tr_plural('elements', 1, '1 element')}")
    print(f"5 elementów: {tr_plural('elements', 5, '5 elementów')}")


def demonstrate_convenience_functions():
    """Demonstrate convenience functions"""
    print("\n=== Convenience Functions ===")
    
    from app.i18n.translation_manager import tr_msg, tr_error, tr_dialog
    
    set_language("en")
    print(f"Success message: {tr_msg('success')}")
    print(f"Error message: {tr_error('file_not_found')}")
    print(f"Dialog button: {tr_dialog('ok')}")
    
    set_language("pl")
    print(f"Success message: {tr_msg('success')}")
    print(f"Error message: {tr_error('file_not_found')}")
    print(f"Dialog button: {tr_dialog('ok')}")


def demonstrate_language_management():
    """Demonstrate language management"""
    print("\n=== Language Management ===")
    
    from app.i18n.translation_manager import get_available_languages, get_current_language
    
    print(f"Available languages: {get_available_languages()}")
    print(f"Current language: {get_current_language()}")
    
    # Test language switching
    set_language("en")
    print(f"After setting English: {get_current_language()}")
    
    set_language("pl")
    print(f"After setting Polish: {get_current_language()}")


def run_example_app():
    """Run the example application"""
    app = QApplication(sys.argv)
    
    # Create and show the example window
    window = ExampleWindow()
    window.show()
    
    return app.exec()


def main():
    """Main function to run all demonstrations"""
    print("PyQt MVVM i18n System Demonstration")
    print("=" * 50)
    
    # Run demonstrations
    demonstrate_basic_usage()
    demonstrate_plural_forms()
    demonstrate_convenience_functions()
    demonstrate_language_management()
    
    print("\n" + "=" * 50)
    print("Starting example application...")
    print("Use the language selectors to change languages")
    
    # Run the example application
    return run_example_app()


if __name__ == "__main__":
    sys.exit(main()) 
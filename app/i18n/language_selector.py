"""
Language Selector Widget

This module provides a language selector widget that can be used
in the application UI to allow users to change languages.
"""

from typing import Optional, Callable
from PyQt6.QtWidgets import (
    QWidget, QComboBox, QHBoxLayout, QLabel, QPushButton,
    QVBoxLayout, QGroupBox, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon

from .translation_manager import get_translation_manager, tr, set_language


class LanguageSelector(QWidget):
    """Language selector widget"""
    
    language_changed = pyqtSignal(str)  # Emitted when language changes
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.translation_manager = get_translation_manager()
        self._setup_ui()
        self._load_languages()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Language selection group
        group_box = QGroupBox(tr("languages.language", "Language"))
        group_layout = QVBoxLayout(group_box)
        
        # Language combo box
        self.language_combo = QComboBox()
        self.language_combo.setMinimumWidth(150)
        group_layout.addWidget(self.language_combo)
        
        # Apply button
        self.apply_button = QPushButton(tr("dialogs.apply", "Apply"))
        self.apply_button.setEnabled(False)
        group_layout.addWidget(self.apply_button)
        
        layout.addWidget(group_box)
        layout.addStretch()
    
    def _load_languages(self):
        """Load available languages into the combo box"""
        self.language_combo.clear()
        
        available_languages = self.translation_manager.get_available_languages()
        current_language = self.translation_manager.get_current_language()
        
        for lang_code in available_languages:
            language_name = self.translation_manager.service.get_language_name(lang_code)
            self.language_combo.addItem(language_name, lang_code)
            
            # Select current language
            if lang_code == current_language:
                self.language_combo.setCurrentIndex(self.language_combo.count() - 1)
    
    def _connect_signals(self):
        """Connect widget signals"""
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        self.apply_button.clicked.connect(self._apply_language)
    
    def _on_language_changed(self, index: int):
        """Handle language selection change"""
        if index >= 0:
            self.apply_button.setEnabled(True)
    
    def _apply_language(self):
        """Apply the selected language"""
        index = self.language_combo.currentIndex()
        if index >= 0:
            language_code = self.language_combo.itemData(index)
            
            # Set the language
            success = set_language(language_code)
            
            if success:
                # Show confirmation message
                QMessageBox.information(
                    self,
                    tr("messages.success", "Success"),
                    tr("messages.language_changed", "Language changed successfully")
                )
                
                # Emit signal
                self.language_changed.emit(language_code)
                
                # Disable apply button
                self.apply_button.setEnabled(False)
            else:
                # Show error message
                QMessageBox.critical(
                    self,
                    tr("messages.error", "Error"),
                    tr("errors.language_change_failed", "Failed to change language")
                )
    
    def refresh(self):
        """Refresh the language selector"""
        self._load_languages()
        self.apply_button.setEnabled(False)


class CompactLanguageSelector(QWidget):
    """Compact language selector for toolbars and status bars"""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.translation_manager = get_translation_manager()
        self._setup_ui()
        self._load_languages()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the compact user interface"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Language label
        self.language_label = QLabel(tr("languages.language", "Language"))
        layout.addWidget(self.language_label)
        
        # Language combo box
        self.language_combo = QComboBox()
        self.language_combo.setMaximumWidth(120)
        layout.addWidget(self.language_combo)
        
        layout.addStretch()
    
    def _load_languages(self):
        """Load available languages"""
        self.language_combo.clear()
        
        available_languages = self.translation_manager.get_available_languages()
        current_language = self.translation_manager.get_current_language()
        
        for lang_code in available_languages:
            language_name = self.translation_manager.service.get_language_name(lang_code)
            self.language_combo.addItem(language_name, lang_code)
            
            if lang_code == current_language:
                self.language_combo.setCurrentIndex(self.language_combo.count() - 1)
    
    def _connect_signals(self):
        """Connect signals"""
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
    
    def _on_language_changed(self, index: int):
        """Handle language change"""
        if index >= 0:
            language_code = self.language_combo.itemData(index)
            success = set_language(language_code)
            
            if success:
                self.language_changed.emit(language_code)
            else:
                # Revert selection on failure
                self._load_languages()
    
    def refresh(self):
        """Refresh the selector"""
        self._load_languages()


class LanguageSettingsWidget(QWidget):
    """Language settings widget for preferences dialog"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.translation_manager = get_translation_manager()
        self._setup_ui()
        self._load_settings()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the settings interface"""
        layout = QVBoxLayout(self)
        
        # Language group
        language_group = QGroupBox(tr("settings.language", "Language"))
        language_layout = QVBoxLayout(language_group)
        
        # Language selector
        self.language_selector = LanguageSelector()
        language_layout.addWidget(self.language_selector)
        
        # Auto-detect option
        self.auto_detect_checkbox = QComboBox()
        self.auto_detect_checkbox.addItem(tr("languages.auto_detect", "Auto-detect"), "auto")
        self.auto_detect_checkbox.addItem(tr("languages.system_language", "System Language"), "system")
        self.auto_detect_checkbox.addItem(tr("languages.manual", "Manual Selection"), "manual")
        language_layout.addWidget(self.auto_detect_checkbox)
        
        layout.addWidget(language_group)
        
        # Information group
        info_group = QGroupBox(tr("common.details", "Details"))
        info_layout = QVBoxLayout(info_group)
        
        self.current_language_label = QLabel()
        self.available_languages_label = QLabel()
        
        info_layout.addWidget(self.current_language_label)
        info_layout.addWidget(self.available_languages_label)
        
        layout.addWidget(info_group)
        layout.addStretch()
    
    def _load_settings(self):
        """Load current settings"""
        current_lang = self.translation_manager.get_current_language()
        available_langs = self.translation_manager.get_available_languages()
        
        # Update labels
        self.current_language_label.setText(
            f"{tr('languages.language', 'Language')}: {self.translation_manager.service.get_language_name(current_lang)}"
        )
        
        available_names = [self.translation_manager.service.get_language_name(lang) for lang in available_langs]
        self.available_languages_label.setText(
            f"{tr('languages.available', 'Available')}: {', '.join(available_names)}"
        )
    
    def _connect_signals(self):
        """Connect signals"""
        self.language_selector.language_changed.connect(self._on_language_changed)
    
    def _on_language_changed(self, language_code: str):
        """Handle language change"""
        self._load_settings()
    
    def apply_settings(self):
        """Apply the current settings"""
        # This could save settings to configuration
        pass
    
    def reset_settings(self):
        """Reset to default settings"""
        # Reset to system language or English
        system_lang = self.translation_manager.service.get_system_language()
        if system_lang in self.translation_manager.get_available_languages():
            set_language(system_lang)
        else:
            set_language("en")
        
        self._load_settings()
        self.language_selector.refresh() 
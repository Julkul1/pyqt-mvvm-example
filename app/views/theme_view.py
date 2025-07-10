from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
    QPushButton, QLabel, QGroupBox, QGridLayout,
    QColorDialog, QMessageBox, QLineEdit, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColor

from app.view_models.theme_view_model import ThemeViewModel


class ThemeView(QWidget):
    """View for theme management"""
    
    theme_applied = pyqtSignal(str)  # Signal when theme is applied
    
    def __init__(self, theme_view_model: ThemeViewModel):
        super().__init__()
        self._view_model = theme_view_model
        self._setup_ui()
        self._connect_signals()
        self._update_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        
        # Theme selection group
        theme_group = QGroupBox("Theme Selection")
        theme_layout = QVBoxLayout()
        
        # Current theme display
        current_layout = QHBoxLayout()
        current_layout.addWidget(QLabel("Current Theme:"))
        self._current_theme_label = QLabel()
        self._current_theme_label.setStyleSheet("font-weight: bold; color: #0078d4;")
        current_layout.addWidget(self._current_theme_label)
        current_layout.addStretch()
        theme_layout.addLayout(current_layout)
        
        # Theme selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Theme:"))
        self._theme_combo = QComboBox()
        self._theme_combo.setMinimumWidth(200)
        selector_layout.addWidget(self._theme_combo)
        
        self._apply_button = QPushButton("Apply")
        self._apply_button.setEnabled(False)
        selector_layout.addWidget(self._apply_button)
        
        selector_layout.addStretch()
        theme_layout.addLayout(selector_layout)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Theme preview group
        preview_group = QGroupBox("Theme Preview")
        preview_layout = QVBoxLayout()
        
        self._preview_widget = QWidget()
        self._preview_widget.setMinimumHeight(200)
        self._preview_widget.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")
        
        preview_inner_layout = QVBoxLayout()
        preview_inner_layout.setContentsMargins(20, 20, 20, 20)
        
        # Preview title
        title_label = QLabel("Theme Preview")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        preview_inner_layout.addWidget(title_label)
        
        # Preview buttons
        button_layout = QHBoxLayout()
        preview_button1 = QPushButton("Primary Button")
        preview_button2 = QPushButton("Secondary Button")
        button_layout.addWidget(preview_button1)
        button_layout.addWidget(preview_button2)
        button_layout.addStretch()
        preview_inner_layout.addLayout(button_layout)
        
        # Preview input
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Input:"))
        preview_input = QLineEdit()
        preview_input.setPlaceholderText("Enter text here...")
        preview_input.setMinimumWidth(200)
        input_layout.addWidget(preview_input)
        input_layout.addStretch()
        preview_inner_layout.addLayout(input_layout)
        
        preview_inner_layout.addStretch()
        self._preview_widget.setLayout(preview_inner_layout)
        
        preview_layout.addWidget(self._preview_widget)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)
        
        # Theme management group
        management_group = QGroupBox("Theme Management")
        management_layout = QVBoxLayout()
        
        # Create theme section
        create_layout = QGridLayout()
        create_layout.addWidget(QLabel("Theme Name:"), 0, 0)
        self._new_theme_name = QLineEdit()
        self._new_theme_name.setPlaceholderText("Enter theme name...")
        create_layout.addWidget(self._new_theme_name, 0, 1)
        
        create_layout.addWidget(QLabel("Description:"), 1, 0)
        self._new_theme_desc = QLineEdit()
        self._new_theme_desc.setPlaceholderText("Enter theme description...")
        create_layout.addWidget(self._new_theme_desc, 1, 1)
        
        self._create_button = QPushButton("Create Theme")
        self._create_button.setEnabled(False)
        create_layout.addWidget(self._create_button, 2, 0, 1, 2)
        
        management_layout.addLayout(create_layout)
        
        # Delete theme section
        delete_layout = QHBoxLayout()
        delete_layout.addWidget(QLabel("Delete Theme:"))
        self._delete_combo = QComboBox()
        self._delete_combo.setMinimumWidth(150)
        delete_layout.addWidget(self._delete_combo)
        
        self._delete_button = QPushButton("Delete")
        self._delete_button.setEnabled(False)
        delete_layout.addWidget(self._delete_button)
        delete_layout.addStretch()
        
        management_layout.addLayout(delete_layout)
        management_group.setLayout(management_layout)
        layout.addWidget(management_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _connect_signals(self):
        """Connect signals and slots"""
        self._theme_combo.currentTextChanged.connect(self._on_theme_selected)
        self._apply_button.clicked.connect(self._on_apply_theme)
        self._create_button.clicked.connect(self._on_create_theme)
        self._delete_button.clicked.connect(self._on_delete_theme)
        
        # Connect view model signals
        self._view_model.themes_changed.connect(self._update_ui)
        self._view_model.current_theme_changed.connect(self._update_ui)
        
        # Connect input validation
        self._new_theme_name.textChanged.connect(self._validate_create_inputs)
        self._new_theme_desc.textChanged.connect(self._validate_create_inputs)
        self._delete_combo.currentTextChanged.connect(self._validate_delete_input)
    
    def _update_ui(self):
        """Update the user interface"""
        # Update theme combo
        current_themes = self._view_model.available_themes
        self._theme_combo.clear()
        self._theme_combo.addItems(current_themes)
        
        # Set current theme
        current_theme = self._view_model.current_theme
        index = self._theme_combo.findText(current_theme)
        if index >= 0:
            self._theme_combo.setCurrentIndex(index)
        
        # Update current theme label
        self._current_theme_label.setText(current_theme)
        
        # Update delete combo
        self._delete_combo.clear()
        deletable_themes = [t for t in current_themes if t != "default"]
        self._delete_combo.addItems(deletable_themes)
        
        # Update preview
        self._update_preview()
    
    def _on_theme_selected(self, theme_name: str):
        """Handle theme selection"""
        self._apply_button.setEnabled(theme_name != self._view_model.current_theme)
        self._update_preview()
    
    def _on_apply_theme(self):
        """Handle theme application"""
        theme_name = self._theme_combo.currentText()
        if theme_name:
            success = self._view_model.apply_theme(theme_name)
            if success:
                self.theme_applied.emit(theme_name)
                self._apply_button.setEnabled(False)
    
    def _on_create_theme(self):
        """Handle theme creation"""
        name = self._new_theme_name.text().strip()
        description = self._new_theme_desc.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a theme name.")
            return
        
        # For now, create a simple theme with default colors
        # In a real app, you might want a color picker dialog
        colors = {
            "background": "#f5f5f5",
            "text": "#333333",
            "primary": "#0078d4",
            "button_text": "#ffffff",
            "input_bg": "#ffffff",
            "border": "#e0e0e0",
            "window_bg": "#ffffff",
            "tab_bg": "#f8f9fa",
            "tab_text": "#666666",
            "primary_hover": "#106ebe"
        }
        
        success = self._view_model.create_theme(name, description, colors)
        if success:
            self._new_theme_name.clear()
            self._new_theme_desc.clear()
            QMessageBox.information(self, "Success", f"Theme '{name}' created successfully!")
        else:
            QMessageBox.warning(self, "Error", f"Failed to create theme '{name}'.")
    
    def _on_delete_theme(self):
        """Handle theme deletion"""
        theme_name = self._delete_combo.currentText()
        if not theme_name:
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to delete the theme '{theme_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self._view_model.delete_theme(theme_name)
            if success:
                QMessageBox.information(self, "Success", f"Theme '{theme_name}' deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete theme '{theme_name}'.")
    
    def _validate_create_inputs(self):
        """Validate create theme inputs"""
        name_valid = bool(self._new_theme_name.text().strip())
        desc_valid = bool(self._new_theme_desc.text().strip())
        self._create_button.setEnabled(name_valid and desc_valid)
    
    def _validate_delete_input(self):
        """Validate delete theme input"""
        theme_name = self._delete_combo.currentText()
        self._delete_button.setEnabled(bool(theme_name))
    
    def _update_preview(self):
        """Update the theme preview"""
        theme_name = self._theme_combo.currentText()
        if not theme_name:
            return
        
        theme_info = self._view_model.get_theme_info(theme_name)
        if not theme_info:
            return
        
        # Apply theme to preview widget
        colors = theme_info.get("colors", {})
        stylesheet = f"""
        QWidget {{
            background-color: {colors.get('background', '#f5f5f5')};
            color: {colors.get('text', '#333333')};
        }}
        QPushButton {{
            background-color: {colors.get('primary', '#0078d4')};
            color: {colors.get('button_text', '#ffffff')};
            border: 1px solid {colors.get('primary', '#0078d4')};
            border-radius: 4px;
            padding: 8px 16px;
        }}
        QPushButton:hover {{
            background-color: {colors.get('primary_hover', '#106ebe')};
        }}
        QLineEdit {{
            background-color: {colors.get('input_bg', '#ffffff')};
            color: {colors.get('text', '#333333')};
            border: 1px solid {colors.get('border', '#d0d0d0')};
            border-radius: 4px;
            padding: 6px;
        }}
        """
        self._preview_widget.setStyleSheet(stylesheet) 
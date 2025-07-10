from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QGroupBox,
                             QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from app.view_models.fuzzy_system_view_model import FuzzySystemViewModel


class SystemView(QWidget):
    """View for system configuration"""
    
    def __init__(self, view_model: FuzzySystemViewModel):
        super().__init__()
        self._view_model = view_model
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        
        # System information group
        system_group = QGroupBox("System Information")
        system_layout = QFormLayout(system_group)
        
        self.name_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        
        system_layout.addRow("Name:", self.name_edit)
        system_layout.addRow("Description:", self.description_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.new_system_btn = QPushButton("New System")
        self.save_system_btn = QPushButton("Save System")
        self.load_system_btn = QPushButton("Load System")
        
        button_layout.addWidget(self.new_system_btn)
        button_layout.addWidget(self.save_system_btn)
        button_layout.addWidget(self.load_system_btn)
        button_layout.addStretch()
        
        # System status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self.status_label = QLabel("No system loaded")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        # Add to main layout
        layout.addWidget(system_group)
        layout.addLayout(button_layout)
        layout.addLayout(status_layout)
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        self.new_system_btn.clicked.connect(self.on_new_system)
        self.save_system_btn.clicked.connect(self.on_save_system)
        self.load_system_btn.clicked.connect(self.on_load_system)
        
        # Connect view model signals
        self._view_model.system_changed.connect(self.on_system_changed)
        self._view_model.validation_errors_changed.connect(self.on_validation_errors_changed)
    
    def on_new_system(self):
        """Handle new system button click"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a system name")
            return
        
        description = self.description_edit.toPlainText().strip()
        self._view_model.create_new_system(name, description)
    
    def on_save_system(self):
        """Handle save system button click"""
        # TODO: Implement save functionality
        QMessageBox.information(self, "Info", "Save functionality not implemented yet")
    
    def on_load_system(self):
        """Handle load system button click"""
        # TODO: Implement load functionality
        QMessageBox.information(self, "Info", "Load functionality not implemented yet")
    
    def on_system_changed(self, system):
        """Handle system changed event"""
        if system:
            self.name_edit.setText(system.name)
            self.description_edit.setPlainText(system.description)
            self.status_label.setText(f"System: {system.name}")
            self.save_system_btn.setEnabled(True)
        else:
            self.name_edit.clear()
            self.description_edit.clear()
            self.status_label.setText("No system loaded")
            self.save_system_btn.setEnabled(False)
    
    def on_validation_errors_changed(self, errors):
        """Handle validation errors changed event"""
        if errors:
            error_text = "\n".join(errors[:3])  # Show first 3 errors
            if len(errors) > 3:
                error_text += f"\n... and {len(errors) - 3} more errors"
            self.status_label.setText(f"Validation errors: {error_text}")
        else:
            system = self._view_model.get_current_system()
            if system:
                self.status_label.setText(f"System: {system.name} (Valid)")
            else:
                self.status_label.setText("No system loaded") 
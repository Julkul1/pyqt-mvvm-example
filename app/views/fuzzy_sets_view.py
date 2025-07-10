from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QGroupBox, QFormLayout,
                             QComboBox, QDoubleSpinBox, QListWidget, QMessageBox,
                             QSplitter)
from PyQt6.QtCore import Qt
from app.view_models.fuzzy_sets_view_model import FuzzySetsViewModel
from app.domain.entities.fuzzy_set import MembershipFunctionType


class FuzzySetsView(QWidget):
    """View for fuzzy sets editor"""
    
    def __init__(self, view_model: FuzzySetsViewModel):
        super().__init__()
        self._view_model = view_model
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        
        # Create splitter for left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Fuzzy sets list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Fuzzy sets list
        list_group = QGroupBox("Fuzzy Sets")
        list_layout = QVBoxLayout(list_group)
        
        self.fuzzy_sets_list = QListWidget()
        list_layout.addWidget(self.fuzzy_sets_list)
        
        # List buttons
        list_buttons_layout = QHBoxLayout()
        self.remove_set_btn = QPushButton("Remove")
        self.remove_set_btn.setEnabled(False)
        list_buttons_layout.addWidget(self.remove_set_btn)
        list_buttons_layout.addStretch()
        
        list_layout.addLayout(list_buttons_layout)
        left_layout.addWidget(list_group)
        left_layout.addStretch()
        
        # Right panel - Fuzzy set editor
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Create new fuzzy set group
        create_group = QGroupBox("Create New Fuzzy Set")
        create_layout = QFormLayout(create_group)
        
        self.set_name_edit = QLineEdit()
        self.set_type_combo = QComboBox()
        self.set_type_combo.addItems(["Triangular", "Trapezoidal", "Gaussian"])
        
        # Parameters
        self.param_a_spin = QDoubleSpinBox()
        self.param_a_spin.setRange(-1000, 1000)
        self.param_a_spin.setValue(0)
        
        self.param_b_spin = QDoubleSpinBox()
        self.param_b_spin.setRange(-1000, 1000)
        self.param_b_spin.setValue(50)
        
        self.param_c_spin = QDoubleSpinBox()
        self.param_c_spin.setRange(-1000, 1000)
        self.param_c_spin.setValue(100)
        
        self.param_d_spin = QDoubleSpinBox()
        self.param_d_spin.setRange(-1000, 1000)
        self.param_d_spin.setValue(100)
        self.param_d_spin.setVisible(False)  # Only for trapezoidal
        
        # Universe bounds
        self.universe_min_spin = QDoubleSpinBox()
        self.universe_min_spin.setRange(-1000, 1000)
        self.universe_min_spin.setValue(0)
        
        self.universe_max_spin = QDoubleSpinBox()
        self.universe_max_spin.setRange(-1000, 1000)
        self.universe_max_spin.setValue(100)
        
        # Add to form
        create_layout.addRow("Name:", self.set_name_edit)
        create_layout.addRow("Type:", self.set_type_combo)
        create_layout.addRow("Parameter A:", self.param_a_spin)
        create_layout.addRow("Parameter B:", self.param_b_spin)
        create_layout.addRow("Parameter C:", self.param_c_spin)
        create_layout.addRow("Parameter D:", self.param_d_spin)
        create_layout.addRow("Universe Min:", self.universe_min_spin)
        create_layout.addRow("Universe Max:", self.universe_max_spin)
        
        # Create button
        self.create_set_btn = QPushButton("Create Fuzzy Set")
        create_layout.addRow("", self.create_set_btn)
        
        right_layout.addWidget(create_group)
        
        # Validation errors
        self.validation_label = QLabel()
        self.validation_label.setStyleSheet("color: red;")
        self.validation_label.setWordWrap(True)
        right_layout.addWidget(self.validation_label)
        
        right_layout.addStretch()
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 400])  # Set initial sizes
        
        layout.addWidget(splitter)
        
        # Connect type combo to show/hide parameters
        self.set_type_combo.currentTextChanged.connect(self.on_type_changed)
        self.on_type_changed("Triangular")  # Set initial state
    
    def setup_connections(self):
        """Setup signal connections"""
        self.create_set_btn.clicked.connect(self.on_create_fuzzy_set)
        self.remove_set_btn.clicked.connect(self.on_remove_fuzzy_set)
        self.fuzzy_sets_list.currentRowChanged.connect(self.on_fuzzy_set_selected)
        
        # Connect view model signals
        self._view_model.fuzzy_sets_changed.connect(self.on_fuzzy_sets_changed)
        self._view_model.validation_errors_changed.connect(self.on_validation_errors_changed)
    
    def on_type_changed(self, type_name: str):
        """Handle fuzzy set type change"""
        if type_name == "Triangular":
            self.param_a_spin.setVisible(True)
            self.param_b_spin.setVisible(True)
            self.param_c_spin.setVisible(True)
            self.param_d_spin.setVisible(False)
        elif type_name == "Trapezoidal":
            self.param_a_spin.setVisible(True)
            self.param_b_spin.setVisible(True)
            self.param_c_spin.setVisible(True)
            self.param_d_spin.setVisible(True)
        elif type_name == "Gaussian":
            self.param_a_spin.setVisible(False)
            self.param_b_spin.setVisible(True)  # Center
            self.param_c_spin.setVisible(True)  # Sigma
            self.param_d_spin.setVisible(False)
    
    def on_create_fuzzy_set(self):
        """Handle create fuzzy set button click"""
        name = self.set_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a fuzzy set name")
            return
        
        set_type = self.set_type_combo.currentText()
        universe_min = self.universe_min_spin.value()
        universe_max = self.universe_max_spin.value()
        
        try:
            if set_type == "Triangular":
                a, b, c = self.param_a_spin.value(), self.param_b_spin.value(), self.param_c_spin.value()
                self._view_model.create_triangular_fuzzy_set(name, a, b, c, universe_min, universe_max)
            elif set_type == "Trapezoidal":
                a, b, c, d = (self.param_a_spin.value(), self.param_b_spin.value(),
                             self.param_c_spin.value(), self.param_d_spin.value())
                self._view_model.create_trapezoidal_fuzzy_set(name, a, b, c, d, universe_min, universe_max)
            elif set_type == "Gaussian":
                center, sigma = self.param_b_spin.value(), self.param_c_spin.value()
                self._view_model.create_gaussian_fuzzy_set(name, center, sigma, universe_min, universe_max)
            
            # Clear form
            self.set_name_edit.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create fuzzy set: {e}")
    
    def on_remove_fuzzy_set(self):
        """Handle remove fuzzy set button click"""
        current_row = self.fuzzy_sets_list.currentRow()
        if current_row >= 0:
            fuzzy_sets = self._view_model.get_fuzzy_sets()
            if current_row < len(fuzzy_sets):
                fuzzy_set = fuzzy_sets[current_row]
                reply = QMessageBox.question(self, "Confirm", f"Remove fuzzy set '{fuzzy_set.name}'?")
                if reply == QMessageBox.StandardButton.Yes:
                    self._view_model.remove_fuzzy_set(fuzzy_set.id)
    
    def on_fuzzy_set_selected(self, row: int):
        """Handle fuzzy set selection"""
        if row >= 0:
            fuzzy_sets = self._view_model.get_fuzzy_sets()
            if row < len(fuzzy_sets):
                fuzzy_set = fuzzy_sets[row]
                self._view_model.select_fuzzy_set(fuzzy_set.id)
                self.remove_set_btn.setEnabled(True)
        else:
            self.remove_set_btn.setEnabled(False)
    
    def on_fuzzy_sets_changed(self, fuzzy_sets):
        """Handle fuzzy sets changed event"""
        self.fuzzy_sets_list.clear()
        for fuzzy_set in fuzzy_sets:
            self.fuzzy_sets_list.addItem(f"{fuzzy_set.name} ({fuzzy_set.membership_function_type.value})")
    
    def on_validation_errors_changed(self, errors):
        """Handle validation errors changed event"""
        if errors:
            error_text = "\n".join(errors)
            self.validation_label.setText(f"Validation Errors:\n{error_text}")
        else:
            self.validation_label.clear() 
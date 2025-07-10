from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QMenuBar, QStatusBar
from PyQt6.QtCore import Qt
from app.view_models.fuzzy_system_view_model import FuzzySystemViewModel
from app.services.fuzzy_logic_service import FuzzyLogicService
from app.services.logger_service import LoggerService


class MainWindow(QMainWindow):
    """Main window for Fuzzy Logic Editor"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuzzy Logic Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create services directly
        self.logger = LoggerService()
        self.fuzzy_logic_service = FuzzyLogicService(self.logger)
        
        # Create view model
        self.view_model = FuzzySystemViewModel(self.fuzzy_logic_service, self.logger)
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        
        # Connect signals
        self.setup_connections()
        
        self.logger.info("Fuzzy Logic Editor started")
    
    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget for different sections
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Add tabs (to be implemented)
        self.setup_system_tab()
        self.setup_variables_tab()
        self.setup_fuzzy_sets_tab()
        self.setup_rules_tab()
        self.setup_evaluation_tab()
    
    def setup_system_tab(self):
        """Setup system configuration tab"""
        # TODO: Implement system configuration UI
        system_widget = QWidget()
        self.tab_widget.addTab(system_widget, "System")
    
    def setup_variables_tab(self):
        """Setup variables configuration tab"""
        # TODO: Implement variables configuration UI
        variables_widget = QWidget()
        self.tab_widget.addTab(variables_widget, "Variables")
    
    def setup_fuzzy_sets_tab(self):
        """Setup fuzzy sets configuration tab"""
        # TODO: Implement fuzzy sets configuration UI
        fuzzy_sets_widget = QWidget()
        self.tab_widget.addTab(fuzzy_sets_widget, "Fuzzy Sets")
    
    def setup_rules_tab(self):
        """Setup rules configuration tab"""
        # TODO: Implement rules configuration UI
        rules_widget = QWidget()
        self.tab_widget.addTab(rules_widget, "Rules")
    
    def setup_evaluation_tab(self):
        """Setup system evaluation tab"""
        # TODO: Implement evaluation UI
        evaluation_widget = QWidget()
        self.tab_widget.addTab(evaluation_widget, "Evaluation")
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New System", self.new_system)
        file_menu.addAction("Open System", self.open_system)
        file_menu.addAction("Save System", self.save_system)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Add Input Variable", self.add_input_variable)
        edit_menu.addAction("Add Output Variable", self.add_output_variable)
        edit_menu.addAction("Add Fuzzy Set", self.add_fuzzy_set)
        edit_menu.addAction("Add Rule", self.add_rule)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def setup_connections(self):
        """Setup signal connections"""
        self.view_model.system_changed.connect(self.on_system_changed)
        self.view_model.validation_errors_changed.connect(self.on_validation_errors_changed)
        self.view_model.evaluation_result_changed.connect(self.on_evaluation_result_changed)
    
    def new_system(self):
        """Create new fuzzy system"""
        # TODO: Show dialog for system name and description
        self.view_model.create_new_system("New Fuzzy System")
        self.status_bar.showMessage("New system created")
    
    def open_system(self):
        """Open existing fuzzy system"""
        # TODO: Implement file open dialog
        self.status_bar.showMessage("Open system - not implemented")
    
    def save_system(self):
        """Save current fuzzy system"""
        # TODO: Implement file save dialog
        self.status_bar.showMessage("Save system - not implemented")
    
    def add_input_variable(self):
        """Add input variable"""
        # TODO: Show dialog for variable name
        self.status_bar.showMessage("Add input variable - not implemented")
    
    def add_output_variable(self):
        """Add output variable"""
        # TODO: Show dialog for variable name
        self.status_bar.showMessage("Add output variable - not implemented")
    
    def add_fuzzy_set(self):
        """Add fuzzy set"""
        # TODO: Show dialog for fuzzy set configuration
        self.status_bar.showMessage("Add fuzzy set - not implemented")
    
    def add_rule(self):
        """Add fuzzy rule"""
        # TODO: Show dialog for rule configuration
        self.status_bar.showMessage("Add rule - not implemented")
    
    def show_about(self):
        """Show about dialog"""
        # TODO: Implement about dialog
        self.status_bar.showMessage("About - not implemented")
    
    def on_system_changed(self, system):
        """Handle system changed event"""
        self.setWindowTitle(f"Fuzzy Logic Editor - {system.name}")
        self.status_bar.showMessage(f"System: {system.name}")
    
    def on_validation_errors_changed(self, errors):
        """Handle validation errors changed event"""
        if errors:
            self.status_bar.showMessage(f"Validation errors: {len(errors)}")
        else:
            self.status_bar.showMessage("System is valid")
    
    def on_evaluation_result_changed(self, results):
        """Handle evaluation result changed event"""
        if results:
            result_str = ", ".join([f"{k}: {v:.2f}" for k, v in results.items()])
            self.status_bar.showMessage(f"Evaluation: {result_str}")
        else:
            self.status_bar.showMessage("Evaluation failed")
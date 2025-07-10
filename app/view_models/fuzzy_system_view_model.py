from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, List, Any, Optional
from app.core.interfaces import ILogger
from app.domain.entities.fuzzy_system import FuzzySystem
from app.domain.entities.fuzzy_set import FuzzySet, MembershipFunctionType
from app.domain.entities.fuzzy_rule import FuzzyRule, OperatorType
from app.services.fuzzy_logic_service import FuzzyLogicService


class FuzzySystemViewModel(QObject):
    """View model for fuzzy system editor"""
    
    # Signals
    system_changed = pyqtSignal(object)  # FuzzySystem
    fuzzy_sets_changed = pyqtSignal(list)  # List[FuzzySet]
    rules_changed = pyqtSignal(list)  # List[FuzzyRule]
    variables_changed = pyqtSignal(list, list)  # input_vars, output_vars
    validation_errors_changed = pyqtSignal(list)  # List[str]
    evaluation_result_changed = pyqtSignal(dict)  # Dict[str, float]
    
    def __init__(self, fuzzy_logic_service: FuzzyLogicService, logger: ILogger):
        super().__init__()
        self._fuzzy_logic_service = fuzzy_logic_service
        self._logger = logger
        self._current_system: Optional[FuzzySystem] = None
        self._validation_errors: List[str] = []
        
    def create_new_system(self, name: str, description: str = "") -> None:
        """Create a new fuzzy system"""
        import uuid
        
        self._current_system = FuzzySystem(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )
        
        self._logger.info(f"Created new fuzzy system: {name}")
        self._emit_system_changed()
    
    def add_input_variable(self, variable: str) -> None:
        """Add an input variable to the system"""
        if not self._current_system:
            return
        
        if variable not in self._current_system.input_variables:
            self._current_system.add_input_variable(variable)
            self._logger.info(f"Added input variable: {variable}")
            self._emit_variables_changed()
    
    def add_output_variable(self, variable: str) -> None:
        """Add an output variable to the system"""
        if not self._current_system:
            return
        
        if variable not in self._current_system.output_variables:
            self._current_system.add_output_variable(variable)
            self._logger.info(f"Added output variable: {variable}")
            self._emit_variables_changed()
    
    def create_triangular_fuzzy_set(self, name: str, a: float, b: float, c: float,
                                   universe_min: float = 0, universe_max: float = 100) -> None:
        """Create and add a triangular fuzzy set"""
        if not self._current_system:
            return
        
        fuzzy_set = self._fuzzy_logic_service.create_triangular_fuzzy_set(
            name, a, b, c, universe_min, universe_max
        )
        
        self._current_system.add_fuzzy_set(fuzzy_set)
        self._logger.info(f"Added triangular fuzzy set: {name}")
        self._emit_fuzzy_sets_changed()
        self._validate_system()
    
    def create_trapezoidal_fuzzy_set(self, name: str, a: float, b: float, c: float, d: float,
                                    universe_min: float = 0, universe_max: float = 100) -> None:
        """Create and add a trapezoidal fuzzy set"""
        if not self._current_system:
            return
        
        fuzzy_set = self._fuzzy_logic_service.create_trapezoidal_fuzzy_set(
            name, a, b, c, d, universe_min, universe_max
        )
        
        self._current_system.add_fuzzy_set(fuzzy_set)
        self._logger.info(f"Added trapezoidal fuzzy set: {name}")
        self._emit_fuzzy_sets_changed()
        self._validate_system()
    
    def create_gaussian_fuzzy_set(self, name: str, center: float, sigma: float,
                                 universe_min: float = 0, universe_max: float = 100) -> None:
        """Create and add a Gaussian fuzzy set"""
        if not self._current_system:
            return
        
        fuzzy_set = self._fuzzy_logic_service.create_gaussian_fuzzy_set(
            name, center, sigma, universe_min, universe_max
        )
        
        self._current_system.add_fuzzy_set(fuzzy_set)
        self._logger.info(f"Added Gaussian fuzzy set: {name}")
        self._emit_fuzzy_sets_changed()
        self._validate_system()
    
    def create_rule(self, name: str, antecedent: List[Dict[str, str]], 
                   consequent: Dict[str, str], operator: str = "and") -> None:
        """Create and add a fuzzy rule"""
        if not self._current_system:
            return
        
        rule = self._fuzzy_logic_service.create_rule(name, antecedent, consequent, operator)
        self._current_system.add_rule(rule)
        
        self._logger.info(f"Added fuzzy rule: {name}")
        self._emit_rules_changed()
        self._validate_system()
    
    def evaluate_system(self, inputs: Dict[str, float]) -> None:
        """Evaluate the current system with given inputs"""
        if not self._current_system:
            return
        
        try:
            results = self._fuzzy_logic_service.evaluate_system(self._current_system, inputs)
            self.evaluation_result_changed.emit(results)
            self._logger.info(f"System evaluation completed: {results}")
        except Exception as e:
            self._logger.error(f"System evaluation failed: {e}")
            self.evaluation_result_changed.emit({})
    
    def get_current_system(self) -> Optional[FuzzySystem]:
        """Get the current fuzzy system"""
        return self._current_system
    
    def get_fuzzy_sets(self) -> List[FuzzySet]:
        """Get all fuzzy sets in the current system"""
        if not self._current_system:
            return []
        return list(self._current_system.fuzzy_sets.values())
    
    def get_rules(self) -> List[FuzzyRule]:
        """Get all rules in the current system"""
        if not self._current_system:
            return []
        return self._current_system.rules
    
    def get_input_variables(self) -> List[str]:
        """Get input variables"""
        if not self._current_system:
            return []
        return self._current_system.input_variables
    
    def get_output_variables(self) -> List[str]:
        """Get output variables"""
        if not self._current_system:
            return []
        return self._current_system.output_variables
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        return self._validation_errors
    
    def _validate_system(self) -> None:
        """Validate the current system"""
        if not self._current_system:
            self._validation_errors = []
        else:
            self._validation_errors = self._fuzzy_logic_service.validate_fuzzy_system(self._current_system)
        
        self.validation_errors_changed.emit(self._validation_errors)
    
    def _emit_system_changed(self) -> None:
        """Emit system changed signal"""
        if self._current_system:
            self.system_changed.emit(self._current_system)
    
    def _emit_fuzzy_sets_changed(self) -> None:
        """Emit fuzzy sets changed signal"""
        self.fuzzy_sets_changed.emit(self.get_fuzzy_sets())
    
    def _emit_rules_changed(self) -> None:
        """Emit rules changed signal"""
        self.rules_changed.emit(self.get_rules())
    
    def _emit_variables_changed(self) -> None:
        """Emit variables changed signal"""
        self.variables_changed.emit(self.get_input_variables(), self.get_output_variables()) 
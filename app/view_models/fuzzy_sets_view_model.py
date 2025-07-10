from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Optional
from app.core.interfaces import ILogger
from app.domain.entities.fuzzy_set import FuzzySet, MembershipFunctionType
from app.services.fuzzy_logic_service import FuzzyLogicService


class FuzzySetsViewModel(QObject):
    """View model for fuzzy sets management"""
    
    # Signals
    fuzzy_sets_changed = pyqtSignal(list)  # List[FuzzySet]
    selected_fuzzy_set_changed = pyqtSignal(object)  # FuzzySet
    validation_errors_changed = pyqtSignal(list)  # List[str]
    
    def __init__(self, fuzzy_logic_service: FuzzyLogicService, logger: ILogger):
        super().__init__()
        self._fuzzy_logic_service = fuzzy_logic_service
        self._logger = logger
        self._fuzzy_sets: List[FuzzySet] = []
        self._selected_fuzzy_set: Optional[FuzzySet] = None
        self._validation_errors: List[str] = []
    
    def create_triangular_fuzzy_set(self, name: str, a: float, b: float, c: float,
                                   universe_min: float = 0, universe_max: float = 100) -> None:
        """Create a triangular fuzzy set"""
        try:
            fuzzy_set = self._fuzzy_logic_service.create_triangular_fuzzy_set(
                name, a, b, c, universe_min, universe_max
            )
            self._fuzzy_sets.append(fuzzy_set)
            self._logger.info(f"Created triangular fuzzy set: {name}")
            self._emit_fuzzy_sets_changed()
            self._validate_parameters()
        except Exception as e:
            self._logger.error(f"Failed to create triangular fuzzy set: {e}")
            self._add_validation_error(f"Failed to create fuzzy set: {e}")
    
    def create_trapezoidal_fuzzy_set(self, name: str, a: float, b: float, c: float, d: float,
                                    universe_min: float = 0, universe_max: float = 100) -> None:
        """Create a trapezoidal fuzzy set"""
        try:
            fuzzy_set = self._fuzzy_logic_service.create_trapezoidal_fuzzy_set(
                name, a, b, c, d, universe_min, universe_max
            )
            self._fuzzy_sets.append(fuzzy_set)
            self._logger.info(f"Created trapezoidal fuzzy set: {name}")
            self._emit_fuzzy_sets_changed()
            self._validate_parameters()
        except Exception as e:
            self._logger.error(f"Failed to create trapezoidal fuzzy set: {e}")
            self._add_validation_error(f"Failed to create fuzzy set: {e}")
    
    def create_gaussian_fuzzy_set(self, name: str, center: float, sigma: float,
                                 universe_min: float = 0, universe_max: float = 100) -> None:
        """Create a Gaussian fuzzy set"""
        try:
            fuzzy_set = self._fuzzy_logic_service.create_gaussian_fuzzy_set(
                name, center, sigma, universe_min, universe_max
            )
            self._fuzzy_sets.append(fuzzy_set)
            self._logger.info(f"Created Gaussian fuzzy set: {name}")
            self._emit_fuzzy_sets_changed()
            self._validate_parameters()
        except Exception as e:
            self._logger.error(f"Failed to create Gaussian fuzzy set: {e}")
            self._add_validation_error(f"Failed to create fuzzy set: {e}")
    
    def remove_fuzzy_set(self, fuzzy_set_id: str) -> None:
        """Remove a fuzzy set"""
        self._fuzzy_sets = [fs for fs in self._fuzzy_sets if fs.id != fuzzy_set_id]
        if self._selected_fuzzy_set and self._selected_fuzzy_set.id == fuzzy_set_id:
            self._selected_fuzzy_set = None
            self.selected_fuzzy_set_changed.emit(None)
        
        self._logger.info(f"Removed fuzzy set: {fuzzy_set_id}")
        self._emit_fuzzy_sets_changed()
    
    def select_fuzzy_set(self, fuzzy_set_id: str) -> None:
        """Select a fuzzy set"""
        self._selected_fuzzy_set = next(
            (fs for fs in self._fuzzy_sets if fs.id == fuzzy_set_id), None
        )
        self.selected_fuzzy_set_changed.emit(self._selected_fuzzy_set)
    
    def get_fuzzy_sets(self) -> List[FuzzySet]:
        """Get all fuzzy sets"""
        return self._fuzzy_sets.copy()
    
    def get_selected_fuzzy_set(self) -> Optional[FuzzySet]:
        """Get the selected fuzzy set"""
        return self._selected_fuzzy_set
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        return self._validation_errors.copy()
    
    def _validate_parameters(self) -> None:
        """Validate fuzzy set parameters"""
        self._validation_errors.clear()
        
        for fuzzy_set in self._fuzzy_sets:
            if fuzzy_set.membership_function_type == MembershipFunctionType.TRIANGULAR:
                a, b, c = fuzzy_set.parameters.get('a', 0), fuzzy_set.parameters.get('b', 0), fuzzy_set.parameters.get('c', 0)
                if not (a <= b <= c):
                    self._add_validation_error(f"Triangular fuzzy set '{fuzzy_set.name}': parameters must be a ≤ b ≤ c")
            
            elif fuzzy_set.membership_function_type == MembershipFunctionType.TRAPEZOIDAL:
                a, b, c, d = (fuzzy_set.parameters.get('a', 0), fuzzy_set.parameters.get('b', 0),
                             fuzzy_set.parameters.get('c', 0), fuzzy_set.parameters.get('d', 0))
                if not (a <= b <= c <= d):
                    self._add_validation_error(f"Trapezoidal fuzzy set '{fuzzy_set.name}': parameters must be a ≤ b ≤ c ≤ d")
            
            elif fuzzy_set.membership_function_type == MembershipFunctionType.GAUSSIAN:
                sigma = fuzzy_set.parameters.get('sigma', 0)
                if sigma <= 0:
                    self._add_validation_error(f"Gaussian fuzzy set '{fuzzy_set.name}': sigma must be positive")
        
        self.validation_errors_changed.emit(self._validation_errors)
    
    def _add_validation_error(self, error: str) -> None:
        """Add a validation error"""
        self._validation_errors.append(error)
        self.validation_errors_changed.emit(self._validation_errors)
    
    def _emit_fuzzy_sets_changed(self) -> None:
        """Emit fuzzy sets changed signal"""
        self.fuzzy_sets_changed.emit(self.get_fuzzy_sets()) 
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, List, Optional
from app.domain.entities.fuzzy_system import FuzzySystem
from app.domain.entities.fuzzy_set import FuzzySet
from app.domain.entities.fuzzy_rule import FuzzyRule


class FuzzySystemModel(QObject):
    """Model for fuzzy system data"""
    
    # Signals for data changes
    system_changed = pyqtSignal(object)  # FuzzySystem
    fuzzy_sets_changed = pyqtSignal(list)  # List[FuzzySet]
    rules_changed = pyqtSignal(list)  # List[FuzzyRule]
    variables_changed = pyqtSignal(list, list)  # input_vars, output_vars
    
    def __init__(self):
        super().__init__()
        self._system: Optional[FuzzySystem] = None
    
    def set_system(self, system: FuzzySystem) -> None:
        """Set the current fuzzy system"""
        self._system = system
        self.system_changed.emit(system)
        self._emit_all_changes()
    
    def get_system(self) -> Optional[FuzzySystem]:
        """Get the current fuzzy system"""
        return self._system
    
    def add_fuzzy_set(self, fuzzy_set: FuzzySet) -> None:
        """Add a fuzzy set to the system"""
        if self._system:
            self._system.add_fuzzy_set(fuzzy_set)
            self.fuzzy_sets_changed.emit(self.get_fuzzy_sets())
    
    def remove_fuzzy_set(self, fuzzy_set_id: str) -> None:
        """Remove a fuzzy set from the system"""
        if self._system and fuzzy_set_id in self._system.fuzzy_sets:
            del self._system.fuzzy_sets[fuzzy_set_id]
            self.fuzzy_sets_changed.emit(self.get_fuzzy_sets())
    
    def add_rule(self, rule: FuzzyRule) -> None:
        """Add a rule to the system"""
        if self._system:
            self._system.add_rule(rule)
            self.rules_changed.emit(self.get_rules())
    
    def remove_rule(self, rule_id: str) -> None:
        """Remove a rule from the system"""
        if self._system:
            self._system.rules = [r for r in self._system.rules if r.id != rule_id]
            self.rules_changed.emit(self.get_rules())
    
    def add_input_variable(self, variable: str) -> None:
        """Add an input variable"""
        if self._system:
            self._system.add_input_variable(variable)
            self.variables_changed.emit(self.get_input_variables(), self.get_output_variables())
    
    def add_output_variable(self, variable: str) -> None:
        """Add an output variable"""
        if self._system:
            self._system.add_output_variable(variable)
            self.variables_changed.emit(self.get_input_variables(), self.get_output_variables())
    
    def get_fuzzy_sets(self) -> List[FuzzySet]:
        """Get all fuzzy sets"""
        if not self._system:
            return []
        return list(self._system.fuzzy_sets.values())
    
    def get_rules(self) -> List[FuzzyRule]:
        """Get all rules"""
        if not self._system:
            return []
        return self._system.rules
    
    def get_input_variables(self) -> List[str]:
        """Get input variables"""
        if not self._system:
            return []
        return self._system.input_variables
    
    def get_output_variables(self) -> List[str]:
        """Get output variables"""
        if not self._system:
            return []
        return self._system.output_variables
    
    def _emit_all_changes(self) -> None:
        """Emit all change signals"""
        if self._system:
            self.fuzzy_sets_changed.emit(self.get_fuzzy_sets())
            self.rules_changed.emit(self.get_rules())
            self.variables_changed.emit(self.get_input_variables(), self.get_output_variables()) 
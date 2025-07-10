from PyQt6.QtCore import QObject, pyqtSignal
from typing import List, Dict, Any, Optional
from app.core.interfaces import ILogger
from app.domain.entities.fuzzy_rule import FuzzyRule, OperatorType
from app.services.fuzzy_logic_service import FuzzyLogicService


class RulesViewModel(QObject):
    """View model for fuzzy rules management"""
    
    # Signals
    rules_changed = pyqtSignal(list)  # List[FuzzyRule]
    selected_rule_changed = pyqtSignal(object)  # FuzzyRule
    validation_errors_changed = pyqtSignal(list)  # List[str]
    
    def __init__(self, fuzzy_logic_service: FuzzyLogicService, logger: ILogger):
        super().__init__()
        self._fuzzy_logic_service = fuzzy_logic_service
        self._logger = logger
        self._rules: List[FuzzyRule] = []
        self._selected_rule: Optional[FuzzyRule] = None
        self._validation_errors: List[str] = []
        self._available_variables: List[str] = []
        self._available_fuzzy_sets: List[str] = []
    
    def create_rule(self, name: str, antecedent: List[Dict[str, str]], 
                   consequent: Dict[str, str], operator: str = "and") -> None:
        """Create a new fuzzy rule"""
        try:
            rule = self._fuzzy_logic_service.create_rule(name, antecedent, consequent, operator)
            self._rules.append(rule)
            self._logger.info(f"Created fuzzy rule: {name}")
            self._emit_rules_changed()
            self._validate_rule(rule)
        except Exception as e:
            self._logger.error(f"Failed to create fuzzy rule: {e}")
            self._add_validation_error(f"Failed to create rule: {e}")
    
    def remove_rule(self, rule_id: str) -> None:
        """Remove a fuzzy rule"""
        self._rules = [r for r in self._rules if r.id != rule_id]
        if self._selected_rule and self._selected_rule.id == rule_id:
            self._selected_rule = None
            self.selected_rule_changed.emit(None)
        
        self._logger.info(f"Removed fuzzy rule: {rule_id}")
        self._emit_rules_changed()
    
    def select_rule(self, rule_id: str) -> None:
        """Select a fuzzy rule"""
        self._selected_rule = next(
            (r for r in self._rules if r.id == rule_id), None
        )
        self.selected_rule_changed.emit(self._selected_rule)
    
    def update_rule(self, rule_id: str, name: str = None, antecedent: List[Dict[str, str]] = None,
                   consequent: Dict[str, str] = None, operator: str = None) -> None:
        """Update a fuzzy rule"""
        rule = next((r for r in self._rules if r.id == rule_id), None)
        if not rule:
            return
        
        if name is not None:
            rule.name = name
        if antecedent is not None:
            rule.antecedent = antecedent
        if consequent is not None:
            rule.consequent = consequent
        if operator is not None:
            rule.operator = OperatorType(operator.lower())
        
        self._logger.info(f"Updated fuzzy rule: {rule.name}")
        self._emit_rules_changed()
        self._validate_rule(rule)
    
    def get_rules(self) -> List[FuzzyRule]:
        """Get all rules"""
        return self._rules.copy()
    
    def get_selected_rule(self) -> Optional[FuzzyRule]:
        """Get the selected rule"""
        return self._selected_rule
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        return self._validation_errors.copy()
    
    def set_available_variables(self, variables: List[str]) -> None:
        """Set available variables for rule creation"""
        self._available_variables = variables.copy()
        self._validate_all_rules()
    
    def set_available_fuzzy_sets(self, fuzzy_set_ids: List[str]) -> None:
        """Set available fuzzy sets for rule creation"""
        self._available_fuzzy_sets = fuzzy_set_ids.copy()
        self._validate_all_rules()
    
    def get_available_variables(self) -> List[str]:
        """Get available variables"""
        return self._available_variables.copy()
    
    def get_available_fuzzy_sets(self) -> List[str]:
        """Get available fuzzy sets"""
        return self._available_fuzzy_sets.copy()
    
    def _validate_rule(self, rule: FuzzyRule) -> None:
        """Validate a single rule"""
        errors = []
        
        # Check antecedent
        for condition in rule.antecedent:
            variable = condition.get('variable')
            fuzzy_set_id = condition.get('fuzzy_set_id')
            
            if not variable:
                errors.append(f"Rule '{rule.name}': Missing variable in antecedent")
            elif variable not in self._available_variables:
                errors.append(f"Rule '{rule.name}': Variable '{variable}' not available")
            
            if not fuzzy_set_id:
                errors.append(f"Rule '{rule.name}': Missing fuzzy set ID in antecedent")
            elif fuzzy_set_id not in self._available_fuzzy_sets:
                errors.append(f"Rule '{rule.name}': Fuzzy set '{fuzzy_set_id}' not available")
        
        # Check consequent
        variable = rule.consequent.get('variable')
        fuzzy_set_id = rule.consequent.get('fuzzy_set_id')
        
        if not variable:
            errors.append(f"Rule '{rule.name}': Missing variable in consequent")
        elif variable not in self._available_variables:
            errors.append(f"Rule '{rule.name}': Variable '{variable}' not available")
        
        if not fuzzy_set_id:
            errors.append(f"Rule '{rule.name}': Missing fuzzy set ID in consequent")
        elif fuzzy_set_id not in self._available_fuzzy_sets:
            errors.append(f"Rule '{rule.name}': Fuzzy set '{fuzzy_set_id}' not available")
        
        # Update validation errors
        self._validation_errors = errors
        self.validation_errors_changed.emit(self._validation_errors)
    
    def _validate_all_rules(self) -> None:
        """Validate all rules"""
        all_errors = []
        for rule in self._rules:
            rule_errors = []
            # Validate each rule (simplified validation here)
            if not rule.antecedent:
                rule_errors.append(f"Rule '{rule.name}': No antecedent conditions")
            if not rule.consequent:
                rule_errors.append(f"Rule '{rule.name}': No consequent")
            all_errors.extend(rule_errors)
        
        self._validation_errors = all_errors
        self.validation_errors_changed.emit(self._validation_errors)
    
    def _add_validation_error(self, error: str) -> None:
        """Add a validation error"""
        self._validation_errors.append(error)
        self.validation_errors_changed.emit(self._validation_errors)
    
    def _emit_rules_changed(self) -> None:
        """Emit rules changed signal"""
        self.rules_changed.emit(self.get_rules()) 
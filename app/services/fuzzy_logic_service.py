from typing import Dict, List, Any
from app.core.interfaces import ILogger
from app.domain.entities.fuzzy_system import FuzzySystem
from app.domain.entities.fuzzy_set import FuzzySet, MembershipFunctionType
from app.domain.entities.fuzzy_rule import FuzzyRule, OperatorType, ImplicationType


class FuzzyLogicService:
    """Service for fuzzy logic operations"""
    
    def __init__(self, logger: ILogger):
        self._logger = logger
    
    def create_triangular_fuzzy_set(self, name: str, a: float, b: float, c: float, 
                                   universe_min: float = 0, universe_max: float = 100) -> FuzzySet:
        """Create a triangular fuzzy set"""
        import uuid
        
        fuzzy_set = FuzzySet(
            id=str(uuid.uuid4()),
            name=name,
            universe_min=universe_min,
            universe_max=universe_max,
            membership_function_type=MembershipFunctionType.TRIANGULAR,
            parameters={'a': a, 'b': b, 'c': c}
        )
        
        self._logger.info(f"Created triangular fuzzy set: {name}")
        return fuzzy_set
    
    def create_trapezoidal_fuzzy_set(self, name: str, a: float, b: float, c: float, d: float,
                                    universe_min: float = 0, universe_max: float = 100) -> FuzzySet:
        """Create a trapezoidal fuzzy set"""
        import uuid
        
        fuzzy_set = FuzzySet(
            id=str(uuid.uuid4()),
            name=name,
            universe_min=universe_min,
            universe_max=universe_max,
            membership_function_type=MembershipFunctionType.TRAPEZOIDAL,
            parameters={'a': a, 'b': b, 'c': c, 'd': d}
        )
        
        self._logger.info(f"Created trapezoidal fuzzy set: {name}")
        return fuzzy_set
    
    def create_gaussian_fuzzy_set(self, name: str, center: float, sigma: float,
                                 universe_min: float = 0, universe_max: float = 100) -> FuzzySet:
        """Create a Gaussian fuzzy set"""
        import uuid
        
        fuzzy_set = FuzzySet(
            id=str(uuid.uuid4()),
            name=name,
            universe_min=universe_min,
            universe_max=universe_max,
            membership_function_type=MembershipFunctionType.GAUSSIAN,
            parameters={'center': center, 'sigma': sigma}
        )
        
        self._logger.info(f"Created Gaussian fuzzy set: {name}")
        return fuzzy_set
    
    def create_rule(self, name: str, antecedent: List[Dict[str, str]], 
                   consequent: Dict[str, str], operator: str = "and") -> FuzzyRule:
        """Create a fuzzy rule"""
        import uuid
        
        rule = FuzzyRule(
            id=str(uuid.uuid4()),
            name=name,
            antecedent=antecedent,
            consequent=consequent,
            operator=OperatorType(operator.lower())
        )
        
        self._logger.info(f"Created fuzzy rule: {name}")
        return rule
    
    def validate_fuzzy_system(self, system: FuzzySystem) -> List[str]:
        """Validate a fuzzy system and return list of errors"""
        errors = []
        
        # Check if system has input variables
        if not system.input_variables:
            errors.append("System must have at least one input variable")
        
        # Check if system has output variables
        if not system.output_variables:
            errors.append("System must have at least one output variable")
        
        # Check if system has fuzzy sets
        if not system.fuzzy_sets:
            errors.append("System must have at least one fuzzy set")
        
        # Check if system has rules
        if not system.rules:
            errors.append("System must have at least one rule")
        
        # Validate rules
        for rule in system.rules:
            rule_errors = self._validate_rule(rule, system)
            errors.extend(rule_errors)
        
        return errors
    
    def _validate_rule(self, rule: FuzzyRule, system: FuzzySystem) -> List[str]:
        """Validate a single rule"""
        errors = []
        
        # Check antecedent
        for condition in rule.antecedent:
            variable = condition.get('variable')
            fuzzy_set_id = condition.get('fuzzy_set_id')
            
            if not variable:
                errors.append(f"Rule {rule.name}: Missing variable in antecedent")
            elif variable not in system.input_variables:
                errors.append(f"Rule {rule.name}: Variable '{variable}' not in input variables")
            
            if not fuzzy_set_id:
                errors.append(f"Rule {rule.name}: Missing fuzzy set ID in antecedent")
            elif fuzzy_set_id not in system.fuzzy_sets:
                errors.append(f"Rule {rule.name}: Fuzzy set '{fuzzy_set_id}' not found")
        
        # Check consequent
        variable = rule.consequent.get('variable')
        fuzzy_set_id = rule.consequent.get('fuzzy_set_id')
        
        if not variable:
            errors.append(f"Rule {rule.name}: Missing variable in consequent")
        elif variable not in system.output_variables:
            errors.append(f"Rule {rule.name}: Variable '{variable}' not in output variables")
        
        if not fuzzy_set_id:
            errors.append(f"Rule {rule.name}: Missing fuzzy set ID in consequent")
        elif fuzzy_set_id not in system.fuzzy_sets:
            errors.append(f"Rule {rule.name}: Fuzzy set '{fuzzy_set_id}' not found")
        
        return errors
    
    def evaluate_system(self, system: FuzzySystem, inputs: Dict[str, float]) -> Dict[str, float]:
        """Evaluate a fuzzy system with given inputs"""
        # Validate inputs
        for var in system.input_variables:
            if var not in inputs:
                raise ValueError(f"Missing input variable: {var}")
        
        # Evaluate system
        results = system.evaluate(inputs)
        
        self._logger.info(f"Evaluated fuzzy system '{system.name}' with inputs: {inputs}, results: {results}")
        return results 
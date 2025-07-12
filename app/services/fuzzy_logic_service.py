from typing import Dict, List, Any
from app.core.interfaces import ILogger, IFuzzyLogicService


class FuzzyLogicService(IFuzzyLogicService):
    """Service for fuzzy logic operations"""
    
    def __init__(self, logger: ILogger):
        self._logger = logger
    
    def create_triangular_fuzzy_set(self, name: str, a: float, b: float, c: float, 
                                   universe_min: float = 0, universe_max: float = 100) -> Dict[str, Any]:
        """Create a triangular fuzzy set"""
        import uuid
        
        fuzzy_set = {
            'id': str(uuid.uuid4()),
            'name': name,
            'universe_min': universe_min,
            'universe_max': universe_max,
            'type': 'triangular',
            'parameters': {'a': a, 'b': b, 'c': c}
        }
        
        self._logger.info(f"Created triangular fuzzy set: {name}")
        return fuzzy_set
    
    def create_trapezoidal_fuzzy_set(self, name: str, a: float, b: float, c: float, d: float,
                                    universe_min: float = 0, universe_max: float = 100) -> Dict[str, Any]:
        """Create a trapezoidal fuzzy set"""
        import uuid
        
        fuzzy_set = {
            'id': str(uuid.uuid4()),
            'name': name,
            'universe_min': universe_min,
            'universe_max': universe_max,
            'type': 'trapezoidal',
            'parameters': {'a': a, 'b': b, 'c': c, 'd': d}
        }
        
        self._logger.info(f"Created trapezoidal fuzzy set: {name}")
        return fuzzy_set
    
    def create_gaussian_fuzzy_set(self, name: str, center: float, sigma: float,
                                 universe_min: float = 0, universe_max: float = 100) -> Dict[str, Any]:
        """Create a Gaussian fuzzy set"""
        import uuid
        
        fuzzy_set = {
            'id': str(uuid.uuid4()),
            'name': name,
            'universe_min': universe_min,
            'universe_max': universe_max,
            'type': 'gaussian',
            'parameters': {'center': center, 'sigma': sigma}
        }
        
        self._logger.info(f"Created Gaussian fuzzy set: {name}")
        return fuzzy_set
    
    def create_rule(self, name: str, antecedent: List[Dict[str, str]], 
                   consequent: Dict[str, str], operator: str = "and") -> Dict[str, Any]:
        """Create a fuzzy rule"""
        import uuid
        
        rule = {
            'id': str(uuid.uuid4()),
            'name': name,
            'antecedent': antecedent,
            'consequent': consequent,
            'operator': operator.lower()
        }
        
        self._logger.info(f"Created fuzzy rule: {name}")
        return rule
    
    def validate_fuzzy_system(self, system: Dict[str, Any]) -> List[str]:
        """Validate a fuzzy system and return list of errors"""
        errors = []
        
        # Check if system has input variables
        if not system.get('input_variables', []):
            errors.append("System must have at least one input variable")
        
        # Check if system has output variables
        if not system.get('output_variables', []):
            errors.append("System must have at least one output variable")
        
        # Check if system has fuzzy sets
        if not system.get('fuzzy_sets', {}):
            errors.append("System must have at least one fuzzy set")
        
        # Check if system has rules
        if not system.get('rules', []):
            errors.append("System must have at least one rule")
        
        return errors
    
    def evaluate_system(self, system: Dict[str, Any], inputs: Dict[str, float]) -> Dict[str, float]:
        """Evaluate a fuzzy system with given inputs"""
        # Validate inputs
        input_variables = system.get('input_variables', [])
        for var in input_variables:
            if var not in inputs:
                raise ValueError(f"Missing input variable: {var}")
        
        # Simple evaluation (placeholder)
        results = {}
        output_variables = system.get('output_variables', [])
        for var in output_variables:
            results[var] = 0.0  # Placeholder result
        
        self._logger.info(f"Evaluated fuzzy system '{system.get('name', 'Unknown')}' with inputs: {inputs}, results: {results}")
        return results 
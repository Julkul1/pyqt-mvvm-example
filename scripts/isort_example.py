#!/usr/bin/env python3
"""
Example file to demonstrate isort functionality.

This file shows how isort organizes imports according to the project configuration.
Run 'python scripts/dev.py sort-imports' to see isort in action.
"""

# Standard library imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Third-party imports
import requests
from typing_extensions import Protocol

# First-party imports (your app modules)
from app.models.fuzzy_system_model import FuzzySystemModel
from app.services.configuration_service import ConfigurationService

# Local imports (relative imports within the same module)
from .utils import get_project_root, run_command


def process_data(data: List[str]) -> Dict[str, str]:
    """Process data using various services."""
    result = {}
    for item in data:
        # Simulate processing
        result[item] = f"processed_{item}"
    return result


def main():
    """Main function demonstrating the imports."""
    data = ["item1", "item2", "item3"]
    result = process_data(data)
    
    print(f"Processed {len(result)} items")
    return 0


if __name__ == "__main__":
    main() 
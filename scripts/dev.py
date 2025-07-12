#!/usr/bin/env python3
"""
Development utilities script for pyqt-mvvm-example.

This script provides common development tasks like linting, formatting,
type checking, and code quality checks.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class DevScript:
    """Development utilities for the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.app_dir = self.project_root / "app"
        self.tests_dir = self.project_root / "tests"
    
    def run_command(self, cmd: List[str], description: str) -> bool:
        """Run a command and return success status."""
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'='*60}")
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed with exit code {e.returncode}")
            return False
    
    def format_code(self) -> bool:
        """Format code using black and isort."""
        success = True
        
        # Run black
        success &= self.run_command(
            [sys.executable, "-m", "black", "app", "tests", "scripts"],
            "Code formatting with black"
        )
        
        # Run isort
        success &= self.run_command(
            [sys.executable, "-m", "isort", "app", "tests", "scripts"],
            "Import sorting with isort"
        )
        
        return success
    
    def sort_imports(self) -> bool:
        """Sort imports using isort."""
        return self.run_command(
            [sys.executable, "-m", "isort", "app", "tests", "scripts"],
            "Import sorting with isort"
        )
    
    def lint_code(self) -> bool:
        """Lint code using flake8 and pylint."""
        success = True
        
        # Run flake8
        success &= self.run_command(
            [sys.executable, "-m", "flake8", "app", "tests", "scripts"],
            "Linting with flake8"
        )
        
        # Run pylint
        success &= self.run_command(
            [sys.executable, "-m", "pylint", "app", "tests", "scripts"],
            "Linting with pylint"
        )
        
        return success
    
    def type_check(self) -> bool:
        """Run type checking with mypy."""
        return self.run_command(
            [sys.executable, "-m", "mypy", "app"],
            "Type checking with mypy"
        )
    
    def run_tests(self, coverage: bool = False, verbose: bool = False) -> bool:
        """Run tests with optional coverage."""
        cmd = [sys.executable, "-m", "pytest"]
        
        if coverage:
            cmd.extend(["--cov=app", "--cov-report=html", "--cov-report=term"])
        
        if verbose:
            cmd.append("-v")
        
        return self.run_command(cmd, "Running tests")
    
    def check_all(self) -> bool:
        """Run all code quality checks."""
        print("🔍 Running all code quality checks...")
        
        success = True
        success &= self.format_code()
        success &= self.lint_code()
        success &= self.type_check()
        success &= self.run_tests(coverage=True)
        
        if success:
            print("\n🎉 All checks passed!")
        else:
            print("\n💥 Some checks failed!")
        
        return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Development utilities")
    parser.add_argument(
        "command",
        choices=["format", "sort-imports", "lint", "type-check", "test", "check-all"],
        help="Command to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Include coverage report when running tests"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    dev_script = DevScript()
    
    if args.command == "format":
        success = dev_script.format_code()
    elif args.command == "sort-imports":
        success = dev_script.sort_imports()
    elif args.command == "lint":
        success = dev_script.lint_code()
    elif args.command == "type-check":
        success = dev_script.type_check()
    elif args.command == "test":
        success = dev_script.run_tests(coverage=args.coverage, verbose=args.verbose)
    elif args.command == "check-all":
        success = dev_script.check_all()
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 
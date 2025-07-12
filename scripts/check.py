#!/usr/bin/env python3
"""
Health check script for pyqt-mvvm-example.

This script performs comprehensive health checks on the project,
including dependency validation, configuration verification,
and system compatibility checks.
"""

import argparse
import importlib
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class HealthCheckScript:
    """Health check utilities for the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.required_deps = [
            "PyQt6",
            "pytest",
            "black",
            "flake8",
            "mypy",
        ]
        self.optional_deps = [
            "pytest-qt",
            "pytest-cov",
            "pylint",
            "pre-commit",
            "pyinstaller",
            "sphinx",
        ]
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Check Python version compatibility."""
        print("🐍 Checking Python version...")
        
        version = sys.version_info
        min_version = (3, 8)
        
        if version >= min_version:
            return True, f"Python {version.major}.{version.minor}.{version.micro} ✓"
        else:
            return False, f"Python {version.major}.{version.minor}.{version.micro} ✗ (requires 3.8+)"
    
    def check_dependencies(self, optional: bool = False) -> Dict[str, Tuple[bool, str]]:
        """Check if dependencies are installed."""
        deps = self.optional_deps if optional else self.required_deps
        deps_type = "optional" if optional else "required"
        
        print(f"📦 Checking {deps_type} dependencies...")
        
        results = {}
        for dep in deps:
            try:
                module = importlib.import_module(dep.lower().replace("-", "_"))
                version = getattr(module, "__version__", "unknown")
                results[dep] = (True, f"✓ {version}")
            except ImportError:
                results[dep] = (False, "✗ Not installed")
        
        return results
    
    def check_project_structure(self) -> List[Tuple[bool, str]]:
        """Check if project structure is correct."""
        print("📁 Checking project structure...")
        
        required_dirs = [
            "app",
            "app/models",
            "app/services",
            "app/view_models",
            "app/views",
            "tests",
            "docs",
        ]
        
        required_files = [
            "main.py",
            "pyproject.toml",
            "README.md",
            "app/__init__.py",
            "tests/__init__.py",
        ]
        
        results = []
        
        # Check directories
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                results.append((True, f"Directory: {dir_path} ✓"))
            else:
                results.append((False, f"Directory: {dir_path} ✗"))
        
        # Check files
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists() and full_path.is_file():
                results.append((True, f"File: {file_path} ✓"))
            else:
                results.append((False, f"File: {file_path} ✗"))
        
        return results
    
    def check_git_status(self) -> Tuple[bool, str]:
        """Check git repository status."""
        print("🔧 Checking git status...")
        
        try:
            # Check if it's a git repository
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                return False, "Not a git repository ✗"
            
            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                return False, "Working directory not clean ✗"
            else:
                return True, "Clean working directory ✓"
                
        except subprocess.CalledProcessError:
            return False, "Git command failed ✗"
    
    def check_virtual_environment(self) -> Tuple[bool, str]:
        """Check if running in virtual environment."""
        print("🌍 Checking virtual environment...")
        
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return True, "Running in virtual environment ✓"
        else:
            return False, "Not running in virtual environment ✗"
    
    def check_configuration_files(self) -> List[Tuple[bool, str]]:
        """Check configuration files."""
        print("⚙️  Checking configuration files...")
        
        config_files = [
            "pyproject.toml",
            "requirements.txt",
            "pytest.ini",
            ".gitignore",
        ]
        
        results = []
        for config_file in config_files:
            full_path = self.project_root / config_file
            if full_path.exists():
                # Basic syntax check for TOML files
                if config_file.endswith('.toml'):
                    try:
                        import tomllib
                        with open(full_path, 'rb') as f:
                            tomllib.load(f)
                        results.append((True, f"{config_file} ✓ (valid syntax)"))
                    except Exception:
                        results.append((False, f"{config_file} ✗ (invalid syntax)"))
                else:
                    results.append((True, f"{config_file} ✓"))
            else:
                results.append((False, f"{config_file} ✗ (missing)"))
        
        return results
    
    def check_test_setup(self) -> Tuple[bool, str]:
        """Check if tests can be run."""
        print("🧪 Checking test setup...")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # Count test files
                test_files = list(self.project_root.rglob("test_*.py"))
                return True, f"Test setup OK ✓ ({len(test_files)} test files found)"
            else:
                return False, f"Test setup failed ✗ ({result.stderr.strip()})"
                
        except Exception as e:
            return False, f"Test setup error ✗ ({e})"
    
    def check_build_setup(self) -> Tuple[bool, str]:
        """Check if build tools are available."""
        print("🔨 Checking build setup...")
        
        try:
            # Check if build module is available
            import build
            return True, "Build tools available ✓"
        except ImportError:
            return False, "Build tools not available ✗"
    
    def run_all_checks(self) -> Dict[str, List[Tuple[bool, str]]]:
        """Run all health checks."""
        print("🏥 Starting comprehensive health check...")
        print("=" * 60)
        
        results = {}
        
        # Python version
        success, message = self.check_python_version()
        results["python"] = [(success, message)]
        
        # Dependencies
        required_results = self.check_dependencies(optional=False)
        optional_results = self.check_dependencies(optional=True)
        
        results["required_deps"] = [(success, f"{dep}: {msg}") for dep, (success, msg) in required_results.items()]
        results["optional_deps"] = [(success, f"{dep}: {msg}") for dep, (success, msg) in optional_results.items()]
        
        # Project structure
        results["structure"] = self.check_project_structure()
        
        # Git status
        success, message = self.check_git_status()
        results["git"] = [(success, message)]
        
        # Virtual environment
        success, message = self.check_virtual_environment()
        results["venv"] = [(success, message)]
        
        # Configuration
        results["config"] = self.check_configuration_files()
        
        # Test setup
        success, message = self.check_test_setup()
        results["tests"] = [(success, message)]
        
        # Build setup
        success, message = self.check_build_setup()
        results["build"] = [(success, message)]
        
        return results
    
    def print_results(self, results: Dict[str, List[Tuple[bool, str]]]) -> None:
        """Print health check results."""
        print("\n" + "=" * 60)
        print("HEALTH CHECK RESULTS")
        print("=" * 60)
        
        total_checks = 0
        passed_checks = 0
        
        for category, checks in results.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            print("-" * 40)
            
            for success, message in checks:
                total_checks += 1
                if success:
                    passed_checks += 1
                    print(f"  {message}")
                else:
                    print(f"  {message}")
        
        print("\n" + "=" * 60)
        print(f"SUMMARY: {passed_checks}/{total_checks} checks passed")
        
        if passed_checks == total_checks:
            print("🎉 All checks passed! Your project is healthy.")
        else:
            print("⚠️  Some checks failed. Please review the issues above.")
        
        print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Health check utilities")
    parser.add_argument(
        "check",
        nargs="?",
        choices=["python", "deps", "structure", "git", "venv", "config", "tests", "build", "all"],
        default="all",
        help="Type of check to run"
    )
    parser.add_argument(
        "--optional",
        action="store_true",
        help="Include optional dependencies in dependency check"
    )
    
    args = parser.parse_args()
    health_script = HealthCheckScript()
    
    if args.check == "all":
        results = health_script.run_all_checks()
        health_script.print_results(results)
    elif args.check == "python":
        success, message = health_script.check_python_version()
        print(message)
    elif args.check == "deps":
        results = health_script.check_dependencies(optional=args.optional)
        for dep, (success, msg) in results.items():
            print(f"{dep}: {msg}")
    elif args.check == "structure":
        results = health_script.check_project_structure()
        for success, message in results:
            print(message)
    elif args.check == "git":
        success, message = health_script.check_git_status()
        print(message)
    elif args.check == "venv":
        success, message = health_script.check_virtual_environment()
        print(message)
    elif args.check == "config":
        results = health_script.check_configuration_files()
        for success, message in results:
            print(message)
    elif args.check == "tests":
        success, message = health_script.check_test_setup()
        print(message)
    elif args.check == "build":
        success, message = health_script.check_build_setup()
        print(message)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
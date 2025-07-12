#!/usr/bin/env python3
"""
Setup script for pyqt-mvvm-example.

This script handles environment setup, dependency installation,
and project initialization.
"""

import argparse
import subprocess
import sys
import venv
from pathlib import Path
from typing import List, Optional


class SetupScript:
    """Setup utilities for the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_dir = self.project_root / ".venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.pyproject_file = self.project_root / "pyproject.toml"
    
    def create_venv(self, python_path: Optional[str] = None) -> bool:
        """Create virtual environment."""
        print("🐍 Creating virtual environment...")
        
        if self.venv_dir.exists():
            print(f"Virtual environment already exists at {self.venv_dir}")
            return True
        
        try:
            venv.create(
                self.venv_dir,
                with_pip=True,
                python=python_path
            )
            print(f"✅ Virtual environment created at {self.venv_dir}")
            return True
        except Exception as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def get_python_executable(self) -> str:
        """Get the Python executable path for the virtual environment."""
        if sys.platform == "win32":
            return str(self.venv_dir / "Scripts" / "python.exe")
        else:
            return str(self.venv_dir / "bin" / "python")
    
    def get_pip_executable(self) -> str:
        """Get the pip executable path for the virtual environment."""
        if sys.platform == "win32":
            return str(self.venv_dir / "Scripts" / "pip.exe")
        else:
            return str(self.venv_dir / "bin" / "pip")
    
    def install_dependencies(self, dev: bool = False) -> bool:
        """Install project dependencies."""
        print("📦 Installing dependencies...")
        
        pip_exe = self.get_pip_executable()
        
        # Upgrade pip first
        try:
            subprocess.run(
                [pip_exe, "install", "--upgrade", "pip"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to upgrade pip: {e}")
        
        # Install dependencies
        try:
            if self.pyproject_file.exists():
                # Use pyproject.toml for installation
                cmd = [pip_exe, "install", "-e"]
                if dev:
                    cmd.append(".[dev]")
                else:
                    cmd.append(".")
                
                subprocess.run(cmd, cwd=self.project_root, check=True)
            elif self.requirements_file.exists():
                # Fallback to requirements.txt
                subprocess.run(
                    [pip_exe, "install", "-r", str(self.requirements_file)],
                    check=True
                )
            else:
                print("❌ No requirements file found")
                return False
            
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def install_pre_commit(self) -> bool:
        """Install and setup pre-commit hooks."""
        print("🔧 Setting up pre-commit hooks...")
        
        try:
            pip_exe = self.get_pip_executable()
            subprocess.run([pip_exe, "install", "pre-commit"], check=True)
            
            # Install pre-commit hooks
            subprocess.run(
                ["pre-commit", "install"],
                cwd=self.project_root,
                check=True
            )
            
            print("✅ Pre-commit hooks installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup pre-commit: {e}")
            return False
    
    def setup_git_hooks(self) -> bool:
        """Setup additional git hooks."""
        print("🔧 Setting up git hooks...")
        
        hooks_dir = self.project_root / ".git" / "hooks"
        if not hooks_dir.exists():
            print("❌ Git repository not found")
            return False
        
        # Create a simple pre-commit hook
        pre_commit_hook = hooks_dir / "pre-commit"
        hook_content = """#!/bin/sh
# Pre-commit hook for pyqt-mvvm-example

echo "Running pre-commit checks..."

# Run tests
python -m pytest tests/ -v

# Run linting
python -m flake8 app/ tests/ scripts/

# Run type checking
python -m mypy app/

echo "Pre-commit checks completed"
"""
        
        try:
            with open(pre_commit_hook, 'w') as f:
                f.write(hook_content)
            
            # Make executable on Unix-like systems
            if sys.platform != "win32":
                subprocess.run(["chmod", "+x", str(pre_commit_hook)], check=True)
            
            print("✅ Git hooks setup completed")
            return True
        except Exception as e:
            print(f"❌ Failed to setup git hooks: {e}")
            return False
    
    def setup_ide_config(self) -> bool:
        """Setup IDE configuration files."""
        print("⚙️  Setting up IDE configuration...")
        
        # VS Code settings
        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        settings = {
            "python.defaultInterpreterPath": str(self.get_python_executable()),
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.linting.flake8Enabled": True,
            "python.formatting.provider": "black",
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests"],
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            }
        }
        
        import json
        with open(vscode_dir / "settings.json", 'w') as f:
            json.dump(settings, f, indent=2)
        
        print("✅ IDE configuration setup completed")
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Setup utilities")
    parser.add_argument(
        "command",
        choices=["venv", "deps", "pre-commit", "git-hooks", "ide", "all"],
        help="Setup command to run"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Install development dependencies"
    )
    parser.add_argument(
        "--python",
        help="Python executable path for virtual environment"
    )
    
    args = parser.parse_args()
    setup_script = SetupScript()
    
    if args.command == "venv":
        success = setup_script.create_venv(args.python)
    elif args.command == "deps":
        success = setup_script.install_dependencies(dev=args.dev)
    elif args.command == "pre-commit":
        success = setup_script.install_pre_commit()
    elif args.command == "git-hooks":
        success = setup_script.setup_git_hooks()
    elif args.command == "ide":
        success = setup_script.setup_ide_config()
    elif args.command == "all":
        success = True
        success &= setup_script.create_venv(args.python)
        success &= setup_script.install_dependencies(dev=args.dev)
        success &= setup_script.install_pre_commit()
        success &= setup_script.setup_git_hooks()
        success &= setup_script.setup_ide_config()
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 
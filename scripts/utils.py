#!/usr/bin/env python3
"""
Utility functions for pyqt-mvvm-example scripts.

This module provides common helper functions used across
various management scripts.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_python_executable() -> str:
    """Get the appropriate Python executable."""
    return sys.executable


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    check: bool = True,
    capture_output: bool = False,
    text: bool = True
) -> subprocess.CompletedProcess:
    """Run a command with consistent settings."""
    if cwd is None:
        cwd = get_project_root()
    
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        capture_output=capture_output,
        text=text
    )


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def get_venv_python(venv_path: Path) -> str:
    """Get Python executable path for virtual environment."""
    if is_windows():
        return str(venv_path / "Scripts" / "python.exe")
    else:
        return str(venv_path / "bin" / "python")


def get_venv_pip(venv_path: Path) -> str:
    """Get pip executable path for virtual environment."""
    if is_windows():
        return str(venv_path / "Scripts" / "pip.exe")
    else:
        return str(venv_path / "bin" / "pip")


def find_files(pattern: str, directory: Optional[Path] = None) -> List[Path]:
    """Find files matching a pattern."""
    if directory is None:
        directory = get_project_root()
    
    return list(directory.rglob(pattern))


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def check_git_status() -> Tuple[bool, str]:
    """Check git repository status."""
    try:
        result = run_command(
            ["git", "status", "--porcelain"],
            capture_output=True,
            check=False
        )
        
        if result.returncode != 0:
            return False, "Not a git repository"
        
        if result.stdout.strip():
            return False, "Working directory not clean"
        
        return True, "Clean working directory"
    except Exception as e:
        return False, f"Error checking git status: {e}"


def get_git_branch() -> Optional[str]:
    """Get current git branch."""
    try:
        result = run_command(
            ["git", "branch", "--show-current"],
            capture_output=True,
            check=False
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None


def get_git_remote_url() -> Optional[str]:
    """Get git remote URL."""
    try:
        result = run_command(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            check=False
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None


def create_directory(path: Path, parents: bool = True) -> bool:
    """Create directory if it doesn't exist."""
    try:
        path.mkdir(parents=parents, exist_ok=True)
        return True
    except Exception:
        return False


def remove_directory(path: Path) -> bool:
    """Remove directory and its contents."""
    try:
        import shutil
        if path.exists():
            shutil.rmtree(path)
        return True
    except Exception:
        return False


def copy_file(src: Path, dst: Path) -> bool:
    """Copy file from source to destination."""
    try:
        import shutil
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False


def read_file_content(file_path: Path) -> Optional[str]:
    """Read file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def write_file_content(file_path: Path, content: str) -> bool:
    """Write content to file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False


def get_environment_info() -> dict:
    """Get environment information."""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "project_root": str(get_project_root()),
        "working_directory": os.getcwd(),
    }


def print_environment_info():
    """Print environment information."""
    info = get_environment_info()
    print("Environment Information:")
    print("=" * 50)
    for key, value in info.items():
        print(f"{key}: {value}")
    print("=" * 50)


def confirm_action(prompt: str) -> bool:
    """Ask user for confirmation."""
    while True:
        response = input(f"{prompt} (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print("Please enter 'y' or 'n'")


def print_success(message: str):
    """Print success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message."""
    print(f"❌ {message}")


def print_warning(message: str):
    """Print warning message."""
    print(f"⚠️  {message}")


def print_info(message: str):
    """Print info message."""
    print(f"ℹ️  {message}")


def print_header(title: str):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subheader(title: str):
    """Print subsection header."""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}") 
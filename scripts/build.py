#!/usr/bin/env python3
"""
Build script for pyqt-mvvm-example.

This script handles building the application for distribution,
including creating executables and packages.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


class BuildScript:
    """Build utilities for the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
    
    def clean_build(self) -> bool:
        """Clean build artifacts."""
        print("🧹 Cleaning build artifacts...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"Removed {dir_path}")
        
        # Clean Python cache
        for pycache in self.project_root.rglob("__pycache__"):
            shutil.rmtree(pycache)
            print(f"Removed {pycache}")
        
        print("✅ Build artifacts cleaned")
        return True
    
    def build_package(self) -> bool:
        """Build Python package."""
        print("📦 Building Python package...")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "build"],
                cwd=self.project_root,
                check=True
            )
            print("✅ Package built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Package build failed: {e}")
            return False
    
    def build_executable(self, onefile: bool = True, windowed: bool = True) -> bool:
        """Build executable using PyInstaller."""
        print("🔨 Building executable...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name=pyqt-mvvm-example",
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
        ]
        
        if onefile:
            cmd.append("--onefile")
        
        if windowed:
            cmd.append("--windowed")
        
        # Add the main script
        cmd.append(str(self.project_root / "main.py"))
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=True)
            print("✅ Executable built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Executable build failed: {e}")
            return False
    
    def create_installer(self) -> bool:
        """Create installer package (placeholder for future implementation)."""
        print("📋 Creating installer...")
        print("⚠️  Installer creation not implemented yet")
        print("   Consider using tools like Inno Setup (Windows) or")
        print("   create-dmg (macOS) for installer creation")
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build utilities")
    parser.add_argument(
        "command",
        choices=["clean", "package", "exe", "installer", "all"],
        help="Build command to run"
    )
    parser.add_argument(
        "--no-onefile",
        action="store_true",
        help="Don't create single file executable"
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help="Show console window (Windows)"
    )
    
    args = parser.parse_args()
    build_script = BuildScript()
    
    if args.command == "clean":
        success = build_script.clean_build()
    elif args.command == "package":
        success = build_script.build_package()
    elif args.command == "exe":
        success = build_script.build_executable(
            onefile=not args.no_onefile,
            windowed=not args.console
        )
    elif args.command == "installer":
        success = build_script.create_installer()
    elif args.command == "all":
        success = True
        success &= build_script.clean_build()
        success &= build_script.build_package()
        success &= build_script.build_executable()
    else:
        parser.print_help()
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 
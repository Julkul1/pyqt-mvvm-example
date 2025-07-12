#!/usr/bin/env python3
"""
Cleanup script for pyqt-mvvm-example.

This script removes temporary files, build artifacts, cache files,
and other clutter that accumulates during development.
"""

import argparse
import shutil
import sys
from pathlib import Path
from typing import List, Set


class CleanupScript:
    """Cleanup utilities for the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        
        # Common patterns to clean
        self.patterns = {
            "python_cache": ["__pycache__", "*.pyc", "*.pyo", "*.pyd"],
            "build_artifacts": ["build", "dist", "*.egg-info"],
            "coverage": ["htmlcov", ".coverage", "coverage.xml"],
            "test_artifacts": [".pytest_cache", ".tox", ".mypy_cache"],
            "ide_files": [".vscode", ".idea", "*.swp", "*.swo", "*~"],
            "os_files": [".DS_Store", "Thumbs.db", "desktop.ini"],
            "logs": ["*.log", "logs"],
            "temp_files": ["*.tmp", "*.temp", "temp", "tmp"],
        }
    
    def find_files(self, patterns: List[str]) -> Set[Path]:
        """Find files matching patterns."""
        found_files = set()
        
        for pattern in patterns:
            if "*" in pattern:
                # Glob pattern
                for file_path in self.project_root.rglob(pattern):
                    found_files.add(file_path)
            else:
                # Directory or file name
                path = self.project_root / pattern
                if path.exists():
                    found_files.add(path)
        
        return found_files
    
    def remove_path(self, path: Path) -> bool:
        """Remove a file or directory."""
        try:
            if path.is_file():
                path.unlink()
                print(f"🗑️  Removed file: {path.relative_to(self.project_root)}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"🗑️  Removed directory: {path.relative_to(self.project_root)}")
            return True
        except Exception as e:
            print(f"❌ Failed to remove {path}: {e}")
            return False
    
    def clean_python_cache(self, dry_run: bool = False) -> int:
        """Clean Python cache files."""
        print("🐍 Cleaning Python cache files...")
        
        files = self.find_files(self.patterns["python_cache"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} Python cache files")
        return count
    
    def clean_build_artifacts(self, dry_run: bool = False) -> int:
        """Clean build artifacts."""
        print("🔨 Cleaning build artifacts...")
        
        files = self.find_files(self.patterns["build_artifacts"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} build artifacts")
        return count
    
    def clean_coverage(self, dry_run: bool = False) -> int:
        """Clean coverage files."""
        print("📊 Cleaning coverage files...")
        
        files = self.find_files(self.patterns["coverage"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} coverage files")
        return count
    
    def clean_test_artifacts(self, dry_run: bool = False) -> int:
        """Clean test artifacts."""
        print("🧪 Cleaning test artifacts...")
        
        files = self.find_files(self.patterns["test_artifacts"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} test artifacts")
        return count
    
    def clean_ide_files(self, dry_run: bool = False) -> int:
        """Clean IDE files."""
        print("💻 Cleaning IDE files...")
        
        files = self.find_files(self.patterns["ide_files"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} IDE files")
        return count
    
    def clean_os_files(self, dry_run: bool = False) -> int:
        """Clean OS-specific files."""
        print("🖥️  Cleaning OS files...")
        
        files = self.find_files(self.patterns["os_files"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} OS files")
        return count
    
    def clean_logs(self, dry_run: bool = False) -> int:
        """Clean log files."""
        print("📝 Cleaning log files...")
        
        files = self.find_files(self.patterns["logs"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} log files")
        return count
    
    def clean_temp_files(self, dry_run: bool = False) -> int:
        """Clean temporary files."""
        print("🗂️  Cleaning temporary files...")
        
        files = self.find_files(self.patterns["temp_files"])
        count = 0
        
        for file_path in files:
            if not dry_run:
                if self.remove_path(file_path):
                    count += 1
            else:
                print(f"Would remove: {file_path.relative_to(self.project_root)}")
                count += 1
        
        print(f"✅ Cleaned {count} temporary files")
        return count
    
    def clean_all(self, dry_run: bool = False) -> int:
        """Clean all types of files."""
        print("🧹 Starting comprehensive cleanup...")
        
        total_count = 0
        total_count += self.clean_python_cache(dry_run)
        total_count += self.clean_build_artifacts(dry_run)
        total_count += self.clean_coverage(dry_run)
        total_count += self.clean_test_artifacts(dry_run)
        total_count += self.clean_ide_files(dry_run)
        total_count += self.clean_os_files(dry_run)
        total_count += self.clean_logs(dry_run)
        total_count += self.clean_temp_files(dry_run)
        
        print(f"\n🎉 Cleanup completed! Removed {total_count} files/directories")
        return total_count
    
    def show_space_saved(self) -> None:
        """Show space that would be saved by cleanup."""
        print("💾 Calculating space usage...")
        
        total_size = 0
        file_count = 0
        
        for category, patterns in self.patterns.items():
            files = self.find_files(patterns)
            category_size = 0
            
            for file_path in files:
                if file_path.is_file():
                    category_size += file_path.stat().st_size
                elif file_path.is_dir():
                    for subfile in file_path.rglob("*"):
                        if subfile.is_file():
                            category_size += subfile.stat().st_size
            
            if category_size > 0:
                print(f"{category}: {self.format_size(category_size)}")
                total_size += category_size
                file_count += len(files)
        
        print(f"\nTotal: {self.format_size(total_size)} in {file_count} files/directories")
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Cleanup utilities")
    parser.add_argument(
        "command",
        choices=["python", "build", "coverage", "test", "ide", "os", "logs", "temp", "all"],
        help="Type of files to clean"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be cleaned without actually removing files"
    )
    parser.add_argument(
        "--space",
        action="store_true",
        help="Show space usage before cleanup"
    )
    
    args = parser.parse_args()
    cleanup_script = CleanupScript()
    
    if args.space:
        cleanup_script.show_space_saved()
        return 0
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be actually removed")
    
    if args.command == "python":
        cleanup_script.clean_python_cache(args.dry_run)
    elif args.command == "build":
        cleanup_script.clean_build_artifacts(args.dry_run)
    elif args.command == "coverage":
        cleanup_script.clean_coverage(args.dry_run)
    elif args.command == "test":
        cleanup_script.clean_test_artifacts(args.dry_run)
    elif args.command == "ide":
        cleanup_script.clean_ide_files(args.dry_run)
    elif args.command == "os":
        cleanup_script.clean_os_files(args.dry_run)
    elif args.command == "logs":
        cleanup_script.clean_logs(args.dry_run)
    elif args.command == "temp":
        cleanup_script.clean_temp_files(args.dry_run)
    elif args.command == "all":
        cleanup_script.clean_all(args.dry_run)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
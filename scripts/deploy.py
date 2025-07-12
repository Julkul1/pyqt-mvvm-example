#!/usr/bin/env python3
"""
Deployment script for pyqt-mvvm-example.

This script handles release management, version bumping,
and distribution deployment.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class DeployScript:
    """Deployment utilities for the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.pyproject_file = self.project_root / "pyproject.toml"
        self.changelog_file = self.project_root / "CHANGELOG.md"
        self.version_file = self.project_root / "app" / "utils" / "version.py"
    
    def get_current_version(self) -> str:
        """Get current version from pyproject.toml."""
        with open(self.pyproject_file, 'r') as f:
            content = f.read()
            match = re.search(r'version = "([^"]+)"', content)
            if match:
                return match.group(1)
        return "0.0.0"
    
    def bump_version(self, bump_type: str) -> str:
        """Bump version number."""
        current_version = self.get_current_version()
        major, minor, patch = map(int, current_version.split('.'))
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        new_version = f"{major}.{minor}.{patch}"
        
        # Update pyproject.toml
        with open(self.pyproject_file, 'r') as f:
            content = f.read()
        
        content = re.sub(
            r'version = "[^"]+"',
            f'version = "{new_version}"',
            content
        )
        
        with open(self.pyproject_file, 'w') as f:
            f.write(content)
        
        # Update version file if it exists
        if self.version_file.exists():
            version_content = f'''"""
Version information for pyqt-mvvm-example.
"""

__version__ = "{new_version}"
__version_info__ = ({major}, {minor}, {patch})
'''
            with open(self.version_file, 'w') as f:
                f.write(version_content)
        
        print(f"✅ Version bumped from {current_version} to {new_version}")
        return new_version
    
    def create_changelog_entry(self, version: str, changes: List[str]) -> bool:
        """Create changelog entry."""
        if not self.changelog_file.exists():
            # Create initial changelog
            changelog_content = f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [{version}] - {datetime.now().strftime('%Y-%m-%d')}

### Added
- Initial release

### Changed

### Deprecated

### Removed

### Fixed

### Security

"""
        else:
            with open(self.changelog_file, 'r') as f:
                changelog_content = f.read()
            
            # Insert new version entry after [Unreleased]
            unreleased_pattern = r'## \[Unreleased\]\n'
            new_entry = f"""## [Unreleased]

## [{version}] - {datetime.now().strftime('%Y-%m-%d')}

### Added
{chr(10).join(f"- {change}" for change in changes if change.startswith('add:'))}

### Changed
{chr(10).join(f"- {change[6:]}" for change in changes if change.startswith('change:'))}

### Deprecated

### Removed
{chr(10).join(f"- {change[7:]}" for change in changes if change.startswith('remove:'))}

### Fixed
{chr(10).join(f"- {change[5:]}" for change in changes if change.startswith('fix:'))}

### Security

"""
            
            changelog_content = re.sub(
                unreleased_pattern,
                new_entry,
                changelog_content
            )
        
        with open(self.changelog_file, 'w') as f:
            f.write(changelog_content)
        
        print(f"✅ Changelog entry created for version {version}")
        return True
    
    def run_tests(self) -> bool:
        """Run all tests before deployment."""
        print("🧪 Running tests...")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v"],
                cwd=self.project_root,
                check=True
            )
            print("✅ All tests passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False
    
    def build_release(self) -> bool:
        """Build release artifacts."""
        print("🔨 Building release artifacts...")
        
        try:
            # Clean previous builds
            subprocess.run(
                [sys.executable, "scripts/build.py", "clean"],
                cwd=self.project_root,
                check=True
            )
            
            # Build package
            subprocess.run(
                [sys.executable, "scripts/build.py", "package"],
                cwd=self.project_root,
                check=True
            )
            
            # Build executable
            subprocess.run(
                [sys.executable, "scripts/build.py", "exe"],
                cwd=self.project_root,
                check=True
            )
            
            print("✅ Release artifacts built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return False
    
    def create_git_tag(self, version: str, message: str) -> bool:
        """Create git tag for release."""
        print(f"🏷️  Creating git tag v{version}...")
        
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=True)
            
            # Commit changes
            subprocess.run(
                ["git", "commit", "-m", f"Release version {version}"],
                cwd=self.project_root,
                check=True
            )
            
            # Create tag
            subprocess.run(
                ["git", "tag", "-a", f"v{version}", "-m", message],
                cwd=self.project_root,
                check=True
            )
            
            print(f"✅ Git tag v{version} created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operations failed: {e}")
            return False
    
    def push_release(self, version: str) -> bool:
        """Push release to remote repository."""
        print(f"🚀 Pushing release v{version}...")
        
        try:
            # Push commits
            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=self.project_root,
                check=True
            )
            
            # Push tags
            subprocess.run(
                ["git", "push", "origin", f"v{version}"],
                cwd=self.project_root,
                check=True
            )
            
            print(f"✅ Release v{version} pushed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Push failed: {e}")
            return False
    
    def create_release_notes(self, version: str) -> str:
        """Create release notes from changelog."""
        if not self.changelog_file.exists():
            return f"Release {version}"
        
        with open(self.changelog_file, 'r') as f:
            content = f.read()
        
        # Extract version section
        pattern = rf'## \[{version}\].*?(?=## \[|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(0).strip()
        else:
            return f"Release {version}"


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Deployment utilities")
    parser.add_argument(
        "command",
        choices=["bump", "test", "build", "tag", "push", "release"],
        help="Deployment command to run"
    )
    parser.add_argument(
        "--type",
        choices=["major", "minor", "patch"],
        default="patch",
        help="Version bump type"
    )
    parser.add_argument(
        "--changes",
        nargs="+",
        help="List of changes for changelog (format: type:description)"
    )
    parser.add_argument(
        "--message",
        help="Git tag message"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests"
    )
    
    args = parser.parse_args()
    deploy_script = DeployScript()
    
    if args.command == "bump":
        version = deploy_script.bump_version(args.type)
        if args.changes:
            deploy_script.create_changelog_entry(version, args.changes)
    elif args.command == "test":
        success = deploy_script.run_tests()
        return 0 if success else 1
    elif args.command == "build":
        success = deploy_script.build_release()
        return 0 if success else 1
    elif args.command == "tag":
        version = deploy_script.get_current_version()
        message = args.message or f"Release version {version}"
        success = deploy_script.create_git_tag(version, message)
        return 0 if success else 1
    elif args.command == "push":
        version = deploy_script.get_current_version()
        success = deploy_script.push_release(version)
        return 0 if success else 1
    elif args.command == "release":
        # Full release process
        version = deploy_script.bump_version(args.type)
        
        if args.changes:
            deploy_script.create_changelog_entry(version, args.changes)
        
        if not args.skip_tests:
            if not deploy_script.run_tests():
                return 1
        
        if not deploy_script.build_release():
            return 1
        
        message = args.message or f"Release version {version}"
        if not deploy_script.create_git_tag(version, message):
            return 1
        
        if not deploy_script.push_release(version):
            return 1
        
        print(f"\n🎉 Release {version} completed successfully!")
        print(f"Release notes:\n{deploy_script.create_release_notes(version)}")
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
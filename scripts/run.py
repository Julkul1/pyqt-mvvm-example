#!/usr/bin/env python3
"""
Main runner script for pyqt-mvvm-example management tools.

This script provides a unified interface to all project management
scripts and utilities.
"""

import argparse
import sys
from pathlib import Path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PyQt MVVM Example - Project Management Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run.py dev check-all          # Run all development checks
  python scripts/run.py setup all --dev        # Setup complete development environment
  python scripts/run.py build exe              # Build executable
  python scripts/run.py deploy release --type minor  # Create new release
  python scripts/run.py clean all              # Clean all temporary files
  python scripts/run.py check all              # Run all health checks
  python scripts/run.py dev format             # Format code
  python scripts/run.py dev lint               # Lint code
  python scripts/run.py dev type-check         # Run type checking
  python scripts/run.py dev test --coverage    # Run tests with coverage
        """
    )
    
    parser.add_argument(
        "script",
        choices=["dev", "build", "setup", "deploy", "clean", "check"],
        help="Script to run"
    )
    parser.add_argument(
        "command",
        help="Command to execute (see individual script help for options)"
    )
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Additional arguments for the script"
    )
    
    args = parser.parse_args()
    
    # Import the appropriate script module
    try:
        if args.script == "dev":
            from scripts import dev
            sys.argv = [sys.argv[0], args.command] + args.args
            return dev.main()
        elif args.script == "build":
            from scripts import build
            sys.argv = [sys.argv[0], args.command] + args.args
            return build.main()
        elif args.script == "setup":
            from scripts import setup
            sys.argv = [sys.argv[0], args.command] + args.args
            return setup.main()
        elif args.script == "deploy":
            from scripts import deploy
            sys.argv = [sys.argv[0], args.command] + args.args
            return deploy.main()
        elif args.script == "clean":
            from scripts import clean
            sys.argv = [sys.argv[0], args.command] + args.args
            return clean.main()
        elif args.script == "check":
            from scripts import check
            sys.argv = [sys.argv[0], args.command] + args.args
            return check.main()
        else:
            parser.print_help()
            return 1
    except ImportError as e:
        print(f"❌ Error importing script module: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 
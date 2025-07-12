# Project Management Scripts

This directory contains comprehensive management scripts for the PyQt MVVM Example project. These scripts provide a professional development workflow similar to what you'd find in large enterprise projects.

## Quick Start

Use the main runner script for all operations:

```bash
# Run all development checks
python scripts/run.py dev check-all

# Setup complete development environment
python scripts/run.py setup all --dev

# Build executable
python scripts/run.py build exe

# Create new release
python scripts/run.py deploy release --type minor

# Clean all temporary files
python scripts/run.py clean all

# Run all health checks
python scripts/run.py check all
```

## Available Scripts

### 🛠️ Development Script (`dev.py`)

Code quality and development workflow tools.

**Commands:**
- `format` - Format code using black and isort
- `sort-imports` - Sort imports using isort only
- `lint` - Lint code using flake8 and pylint
- `type-check` - Run type checking with mypy
- `test` - Run tests with optional coverage
- `check-all` - Run all code quality checks

**Examples:**
```bash
python scripts/dev.py format
python scripts/dev.py sort-imports
python scripts/dev.py lint
python scripts/dev.py type-check
python scripts/dev.py test --coverage --verbose
python scripts/dev.py check-all
```

### 🔨 Build Script (`build.py`)

Build and packaging utilities.

**Commands:**
- `clean` - Clean build artifacts
- `package` - Build Python package
- `exe` - Build executable using PyInstaller
- `installer` - Create installer package (placeholder)
- `all` - Run all build steps

**Examples:**
```bash
python scripts/build.py clean
python scripts/build.py package
python scripts/build.py exe --no-onefile --console
python scripts/build.py all
```

### ⚙️ Setup Script (`setup.py`)

Environment and dependency management.

**Commands:**
- `venv` - Create virtual environment
- `deps` - Install dependencies
- `pre-commit` - Install pre-commit hooks
- `git-hooks` - Setup git hooks
- `ide` - Setup IDE configuration
- `all` - Run all setup steps

**Examples:**
```bash
python scripts/setup.py venv --python python3.9
python scripts/setup.py deps --dev
python scripts/setup.py pre-commit
python scripts/setup.py ide
python scripts/setup.py all --dev
```

### 🚀 Deploy Script (`deploy.py`)

Release management and deployment.

**Commands:**
- `bump` - Bump version number
- `test` - Run tests before deployment
- `build` - Build release artifacts
- `tag` - Create git tag
- `push` - Push release to remote
- `release` - Complete release process

**Examples:**
```bash
python scripts/deploy.py bump --type minor
python scripts/deploy.py test
python scripts/deploy.py build
python scripts/deploy.py tag --message "Release v1.1.0"
python scripts/deploy.py release --type patch --changes "fix:bug fix" "add:new feature"
```

### 🧹 Cleanup Script (`clean.py`)

File cleanup and maintenance utilities.

**Commands:**
- `python` - Clean Python cache files
- `build` - Clean build artifacts
- `coverage` - Clean coverage files
- `test` - Clean test artifacts
- `ide` - Clean IDE files
- `os` - Clean OS-specific files
- `logs` - Clean log files
- `temp` - Clean temporary files
- `all` - Clean all types of files

**Examples:**
```bash
python scripts/clean.py python
python scripts/clean.py build
python scripts/clean.py all --dry-run
python scripts/clean.py all --space
```

### 🏥 Health Check Script (`check.py`)

Project health and validation utilities.

**Commands:**
- `python` - Check Python version
- `deps` - Check dependencies
- `structure` - Check project structure
- `git` - Check git status
- `venv` - Check virtual environment
- `config` - Check configuration files
- `tests` - Check test setup
- `build` - Check build setup
- `all` - Run all health checks

**Examples:**
```bash
python scripts/check.py python
python scripts/check.py deps --optional
python scripts/check.py structure
python scripts/check.py all
```

### 🛠️ Utilities (`utils.py`)

Common helper functions used across all scripts.

**Features:**
- Project path management
- Command execution utilities
- Platform detection
- File operations
- Git status checking
- Environment information
- User interaction helpers

## Workflow Examples

### Initial Project Setup

```bash
# 1. Create virtual environment and install dependencies
python scripts/run.py setup all --dev

# 2. Run initial code quality checks
python scripts/run.py dev check-all

# 3. Run tests to ensure everything works
python scripts/run.py dev test --coverage
```

### Daily Development Workflow

```bash
# 1. Format and lint code
python scripts/run.py dev format
python scripts/run.py dev lint

# 2. Run type checking
python scripts/run.py dev type-check

# 3. Run tests
python scripts/run.py dev test

# 4. Or run all checks at once
python scripts/run.py dev check-all
```

### Release Process

```bash
# 1. Create new release (bumps version, updates changelog, builds, tags, pushes)
python scripts/run.py deploy release --type minor --changes "add:new feature" "fix:bug fix"

# 2. Or do it step by step
python scripts/run.py deploy bump --type minor
python scripts/run.py deploy test
python scripts/run.py deploy build
python scripts/run.py deploy tag --message "Release v1.1.0"
python scripts/run.py deploy push
```

### Building for Distribution

```bash
# 1. Clean previous builds
python scripts/run.py build clean

# 2. Build package
python scripts/run.py build package

# 3. Build executable
python scripts/run.py build exe

# 4. Or build everything at once
python scripts/run.py build all
```

### Maintenance Workflow

```bash
# 1. Clean up temporary files
python scripts/run.py clean all

# 2. Run health checks
python scripts/run.py check all

# 3. Fix any issues found
# ... manual fixes ...

# 4. Run tests to ensure everything still works
python scripts/run.py dev test
```

## Configuration

### IDE Setup

The setup script automatically configures VS Code with:
- Python interpreter path
- Linting (pylint, flake8)
- Formatting (black)
- Testing (pytest)
- Auto-format on save
- Import organization

### Git Hooks

Pre-commit hooks are automatically installed to:
- Run tests
- Check linting
- Verify type checking

### Environment Variables

The scripts respect these environment variables:
- `PYTHONPATH` - Python path configuration
- `VIRTUAL_ENV` - Virtual environment path

## Troubleshooting

### Common Issues

1. **Script not found**: Ensure you're running from the project root directory
2. **Permission denied**: Make sure scripts are executable (`chmod +x scripts/*.py`)
3. **Import errors**: Ensure all dependencies are installed (`python scripts/setup.py deps --dev`)
4. **Git errors**: Ensure you're in a git repository and have proper permissions

### Getting Help

Each script provides detailed help:

```bash
python scripts/dev.py --help
python scripts/build.py --help
python scripts/setup.py --help
python scripts/deploy.py --help
python scripts/run.py --help
```

## Contributing

When adding new scripts or modifying existing ones:

1. Follow the existing code style and structure
2. Add comprehensive help text and examples
3. Include proper error handling
4. Add tests for new functionality
5. Update this README with new commands and examples

## Script Architecture

The scripts follow a modular design:

```
scripts/
├── __init__.py          # Package initialization
├── run.py              # Main runner script
├── dev.py              # Development utilities
├── build.py            # Build utilities
├── setup.py            # Setup utilities
├── deploy.py           # Deployment utilities
├── clean.py            # Cleanup utilities
├── check.py            # Health check utilities
├── utils.py            # Common utilities
└── README.md           # This file
```

Each script is self-contained but shares common utilities through the `utils.py` module. The `run.py` script provides a unified interface to all other scripts. 
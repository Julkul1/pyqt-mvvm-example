# Contributing to PyQt MVVM Fuzzy Logic Example

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started

### Prerequisites
- Python 3.9 or higher
- PyQt6
- Git

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/pyqt-mvvm-example.git
   cd pyqt-mvvm-example
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original-owner/pyqt-mvvm-example.git
   ```

## Development Setup

### 1. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 3. Install Pre-commit Hooks
```bash
pre-commit install
```

### 4. Run Tests
```bash
pytest
```

## Code Style

### Python Code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for all function parameters and return values
- Keep functions small and focused
- Use descriptive variable and function names
- Add docstrings for all public functions and classes

### Example
```python
from typing import Optional, List

def calculate_membership(x: float, fuzzy_set: FuzzySet) -> float:
    """
    Calculate membership degree for a given value.
    
    Args:
        x: Input value
        fuzzy_set: Fuzzy set to evaluate
        
    Returns:
        Membership degree between 0 and 1
    """
    if x < fuzzy_set.universe_min or x > fuzzy_set.universe_max:
        return 0.0
    
    return fuzzy_set.calculate_membership(x)
```

### File Organization
- Follow the existing project structure
- Keep related functionality together
- Use meaningful file and directory names
- Separate concerns (models, views, view models, services)

### Commit Messages
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(i18n): add Polish language support
fix(fuzzy-sets): resolve membership calculation error
docs(readme): update installation instructions
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies
- Test both success and failure cases

### Example Test
```python
import pytest
from app.models.fuzzy_system_model import FuzzySystem

def test_fuzzy_system_creation():
    """Test that fuzzy system can be created with valid parameters."""
    # Arrange
    name = "Test System"
    description = "A test fuzzy system"
    
    # Act
    system = FuzzySystem(name=name, description=description)
    
    # Assert
    assert system.name == name
    assert system.description == description
    assert len(system.fuzzy_sets) == 0
```

## Pull Request Process

### Before Submitting
1. Ensure your code follows the style guidelines
2. Run all tests and ensure they pass
3. Update documentation if needed
4. Test on multiple platforms if applicable

### Creating a Pull Request
1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit them
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Create a pull request on GitHub
5. Fill out the pull request template
6. Request review from maintainers

### Pull Request Guidelines
- Keep PRs focused and small
- Include tests for new functionality
- Update documentation as needed
- Respond to review comments promptly
- Squash commits before merging if requested

## Issue Reporting

### Before Creating an Issue
1. Search existing issues to avoid duplicates
2. Check the documentation
3. Try to reproduce the issue

### Issue Guidelines
- Use the appropriate issue template
- Provide clear and concise descriptions
- Include steps to reproduce
- Add screenshots if applicable
- Specify your environment details

## Code of Conduct

### Our Standards
- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community
- Show empathy towards other community members

### Enforcement
- Unacceptable behavior will not be tolerated
- Violations will be addressed promptly
- Maintainers have the right to remove, edit, or reject contributions

## Getting Help

### Questions and Discussions
- Use GitHub Discussions for questions
- Search existing issues and discussions
- Be specific about your problem
- Provide relevant code examples

### Communication Channels
- GitHub Issues for bugs and feature requests
- GitHub Discussions for questions and general discussion
- Pull requests for code contributions

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to this project! 
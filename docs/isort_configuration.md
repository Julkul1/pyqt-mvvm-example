# isort Configuration

This document explains the isort configuration used in the PyQt MVVM Example project.

## Overview

isort is a Python utility/library to sort imports alphabetically and automatically separated into sections. It is integrated with Black to ensure consistent code formatting.

## Configuration

The isort configuration is defined in `pyproject.toml`:

```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
known_first_party = ["app"]
known_third_party = ["PyQt6", "pytest", "black", "flake8", "mypy"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

## Configuration Options Explained

### `profile = "black"`
- Uses Black-compatible formatting
- Ensures isort output is compatible with Black

### `line_length = 100`
- Matches the Black line length setting
- Imports will wrap at 100 characters

### `multi_line_output = 3`
- Uses vertical hanging indent style
- Compatible with Black's formatting

### `include_trailing_comma = true`
- Adds trailing commas in multi-line imports
- Matches Black's style

### `force_grid_wrap = 0`
- Disables forced grid wrapping
- Allows natural wrapping

### `use_parentheses = true`
- Uses parentheses for multi-line imports
- Matches Black's style

### `ensure_newline_before_comments = true`
- Ensures comments are on separate lines
- Improves readability

### `known_first_party = ["app"]`
- Identifies `app` as a first-party module
- Imports from `app` will be sorted in the FIRSTPARTY section

### `known_third_party = ["PyQt6", "pytest", "black", "flake8", "mypy"]`
- Identifies specific third-party packages
- These will be sorted in the THIRDPARTY section

### `sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]`
- Defines the order of import sections
- FUTURE: Future imports (e.g., `from __future__ import annotations`)
- STDLIB: Standard library imports
- THIRDPARTY: Third-party package imports
- FIRSTPARTY: Your project's imports
- LOCALFOLDER: Relative imports within the same module

## Import Organization

isort organizes imports into sections in this order:

1. **FUTURE** - Future imports
2. **STDLIB** - Standard library imports
3. **THIRDPARTY** - Third-party package imports
4. **FIRSTPARTY** - Your project's imports (from `app`)
5. **LOCALFOLDER** - Relative imports

### Example

```python
# FUTURE imports
from __future__ import annotations

# STDLIB imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# THIRDPARTY imports
import PyQt6
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow

# FIRSTPARTY imports
from app.core.interfaces import BaseModel
from app.models.fuzzy_system_model import FuzzySystemModel
from app.services.configuration_service import ConfigurationService

# LOCALFOLDER imports
from .utils import get_project_root, run_command
```

## Usage

### Using Management Scripts

```bash
# Format code (runs both black and isort)
python scripts/run.py dev format

# Sort imports only
python scripts/run.py dev sort-imports

# Run all code quality checks
python scripts/run.py dev check-all
```

### Direct Usage

```bash
# Sort imports in specific directories
isort app/ tests/ scripts/

# Check what would be changed (dry run)
isort --check-only app/

# Show diff of changes
isort --diff app/
```

### IDE Integration

Most IDEs support isort integration:

- **VS Code**: Install the "isort" extension
- **PyCharm**: Built-in support for isort
- **Vim/Neovim**: Use plugins like "ale" or "coc"

### Pre-commit Integration

isort is automatically run as part of the pre-commit hooks when you use:

```bash
python scripts/run.py setup pre-commit
```

## Best Practices

1. **Run isort before Black**: isort should be run before Black to ensure compatibility
2. **Use the management scripts**: The scripts ensure proper order and configuration
3. **Check before committing**: Use `--check-only` to verify imports are sorted
4. **IDE integration**: Configure your IDE to run isort on save

## Troubleshooting

### Import Conflicts

If you have import conflicts, you can add specific packages to the configuration:

```toml
[tool.isort]
known_third_party = ["PyQt6", "pytest", "black", "flake8", "mypy", "your_package"]
```

### Custom Sections

For complex projects, you can add custom sections:

```toml
[tool.isort]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER", "CUSTOM"]
known_custom = ["your_custom_package"]
```

### Ignoring Files

To ignore specific files or directories:

```toml
[tool.isort]
skip = ["migrations", "venv", ".venv"]
```

## Related Tools

- **Black**: Code formatter (runs after isort)
- **flake8**: Linter (checks import organization)
- **mypy**: Type checker (validates import types)

For more information, see the [isort documentation](https://pycqa.github.io/isort/). 
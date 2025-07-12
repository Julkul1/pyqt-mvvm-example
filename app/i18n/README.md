# Internationalization (i18n) System

This directory contains the internationalization system for the PyQt MVVM application, providing comprehensive translation support for English and Polish languages.

## Directory Structure

```
app/i18n/
├── __init__.py
├── README.md
├── translation_service.py      # Core translation service
├── translation_manager.py      # Global translation manager
├── language_selector.py        # UI widgets for language selection
└── translations/
    ├── en.json                 # English translations
    └── pl.json                 # Polish translations
```

## Features

- **Multi-language Support**: English (en) and Polish (pl)
- **JSON-based Translations**: Easy to edit and maintain
- **Global Translation Manager**: Singleton pattern for easy access
- **UI Language Selectors**: Widgets for language selection
- **Plural Forms Support**: Handle different plural forms
- **Fallback System**: Graceful fallback to English
- **Qt Integration**: Native PyQt6 translation support
- **Caching**: Performance optimization with LRU cache

## Quick Start

### Basic Usage

```python
from app.i18n.translation_manager import tr, set_language

# Set language
set_language("pl")  # Polish
set_language("en")  # English

# Translate text
title = tr("app.title")
message = tr("messages.success")
error = tr("errors.file_not_found")
```

### Using Convenience Functions

```python
from app.i18n.translation_manager import tr_msg, tr_error, tr_dialog

# Cached translation functions
success_msg = tr_msg("success")
error_msg = tr_error("file_not_found")
ok_button = tr_dialog("ok")
```

### In UI Components

```python
from app.i18n.language_selector import LanguageSelector
from app.i18n.translation_manager import tr

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set translated title
        self.setWindowTitle(tr("main_window.title"))
        
        # Add language selector
        self.language_selector = LanguageSelector()
        self.language_selector.language_changed.connect(self.on_language_changed)
```

## Translation Keys Structure

The translation system uses a hierarchical key structure:

```
app.title                    # Application title
main_window.title           # Main window title
fuzzy_sets.title           # Fuzzy sets section
rules.add_rule             # Add rule button
messages.success           # Success message
errors.file_not_found      # Error message
dialogs.ok                 # Dialog button
common.loading             # Common UI text
```

### Key Categories

- **`app.*`**: Application-level information
- **`main_window.*`**: Main window UI elements
- **`fuzzy_sets.*`**: Fuzzy sets related UI
- **`rules.*`**: Fuzzy rules related UI
- **`system.*`**: System evaluation UI
- **`themes.*`**: Theme selection UI
- **`dialogs.*`**: Dialog box elements
- **`messages.*`**: User messages
- **`errors.*`**: Error messages
- **`languages.*`**: Language-related text
- **`settings.*`**: Settings dialog
- **`help.*`**: Help system
- **`common.*`**: Common UI elements

## Adding New Translations

### 1. Add Translation Keys

Add new keys to both language files:

```json
// en.json
{
  "new_feature": {
    "title": "New Feature",
    "description": "This is a new feature",
    "button": "Enable Feature"
  }
}

// pl.json
{
  "new_feature": {
    "title": "Nowa Funkcja",
    "description": "To jest nowa funkcja",
    "button": "Włącz Funkcję"
  }
}
```

### 2. Use in Code

```python
from app.i18n.translation_manager import tr

title = tr("new_feature.title")
description = tr("new_feature.description")
button_text = tr("new_feature.button")
```

### 3. Add Convenience Function (Optional)

```python
# In translation_manager.py
@lru_cache(maxsize=128)
def tr_new_feature(key: str, default: Optional[str] = None) -> str:
    """Translate new feature elements with caching"""
    return tr(f"new_feature.{key}", default)
```

## Language Selector Widgets

### LanguageSelector

Full-featured language selector with apply button:

```python
from app.i18n.language_selector import LanguageSelector

selector = LanguageSelector()
selector.language_changed.connect(self.on_language_changed)
```

### CompactLanguageSelector

Compact selector for toolbars and status bars:

```python
from app.i18n.language_selector import CompactLanguageSelector

compact_selector = CompactLanguageSelector()
compact_selector.language_changed.connect(self.on_language_changed)
```

### LanguageSettingsWidget

Settings widget for preferences dialog:

```python
from app.i18n.language_selector import LanguageSettingsWidget

settings_widget = LanguageSettingsWidget()
settings_widget.apply_settings()
```

## Integration with MVVM Architecture

### Service Layer

```python
# In app/services/configuration_service.py
from app.i18n.translation_manager import get_translation_manager

class ConfigurationService:
    def __init__(self):
        self.translation_service = get_translation_manager().service
    
    def get_language(self) -> str:
        return self.translation_service.get_current_language()
    
    def set_language(self, language: str) -> bool:
        return self.translation_service.set_language(language)
```

### View Model Layer

```python
# In app/view_models/main_view_model.py
from app.i18n.translation_manager import tr

class MainViewModel:
    def __init__(self):
        self.title = tr("main_window.title")
        self.status = tr("main_window.status.ready")
    
    def update_status(self, status_key: str):
        self.status = tr(f"main_window.status.{status_key}")
```

### View Layer

```python
# In app/views/main_window.py
from app.i18n.translation_manager import tr
from app.i18n.language_selector import CompactLanguageSelector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("main_window.title"))
        
        # Add language selector to toolbar
        self.language_selector = CompactLanguageSelector()
        self.toolbar.addWidget(self.language_selector)
```

## Advanced Features

### Plural Forms

```python
from app.i18n.translation_manager import tr_plural

# English: "1 item" vs "5 items"
# Polish: "1 element" vs "5 elementów"
count = 5
text = tr_plural("items", count, f"{count} items")
```

### Dynamic Translation Updates

```python
from app.i18n.translation_manager import get_translation_manager

def update_ui_texts():
    """Update all UI texts when language changes"""
    manager = get_translation_manager()
    
    # Update window titles
    self.setWindowTitle(tr("main_window.title"))
    
    # Update button texts
    self.save_button.setText(tr("dialogs.save"))
    self.cancel_button.setText(tr("dialogs.cancel"))
    
    # Update labels
    self.status_label.setText(tr("main_window.status.ready"))
```

### Custom Translation Contexts

```python
# Create context-specific translation functions
def tr_fuzzy_system(key: str, default: Optional[str] = None) -> str:
    """Translate fuzzy system specific text"""
    return tr(f"system.{key}", default)

def tr_membership_function(key: str, default: Optional[str] = None) -> str:
    """Translate membership function specific text"""
    return tr(f"fuzzy_sets.{key}", default)
```

## Configuration

### Translation Directory

By default, translations are loaded from the `translations/` directory relative to the application. You can customize this:

```python
from app.i18n.translation_service import TranslationService

# Custom translations directory
service = TranslationService("custom/translations/path")
```

### Language Detection

The system automatically detects the system language:

```python
from app.i18n.translation_manager import get_translation_manager

manager = get_translation_manager()
system_lang = manager.service.get_system_language()

# Automatically set to system language if supported
if system_lang in manager.get_available_languages():
    manager.set_language(system_lang)
```

## Best Practices

### 1. Use Hierarchical Keys

```python
# Good
tr("fuzzy_sets.add_set")
tr("rules.delete_rule")

# Avoid
tr("add_fuzzy_set")
tr("delete_rule")
```

### 2. Provide Default Values

```python
# Always provide fallback text
title = tr("new_feature.title", "New Feature")
```

### 3. Use Cached Functions for Common Patterns

```python
# Use cached functions for frequently accessed translations
from app.i18n.translation_manager import tr_msg, tr_error

success = tr_msg("success")  # Cached
error = tr_error("file_not_found")  # Cached
```

### 4. Handle Missing Translations Gracefully

```python
def safe_translate(key: str, default: str) -> str:
    """Safely translate with fallback"""
    result = tr(key, default)
    if result == key:  # Translation not found
        return default
    return result
```

### 5. Update UI on Language Change

```python
class TranslatableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.translation_manager = get_translation_manager()
        self.translation_manager.language_changed.connect(self.update_texts)
    
    def update_texts(self):
        """Update all text elements when language changes"""
        self.setWindowTitle(tr("widget.title"))
        self.button.setText(tr("widget.button"))
```

## Testing

### Unit Tests

```python
import pytest
from app.i18n.translation_manager import tr, set_language

def test_english_translation():
    set_language("en")
    assert tr("app.title") == "PyQt MVVM Fuzzy Logic Example"

def test_polish_translation():
    set_language("pl")
    assert tr("app.title") == "Przykład PyQt MVVM z Logiką Rozmyta"

def test_missing_translation():
    set_language("en")
    result = tr("nonexistent.key", "Default Text")
    assert result == "Default Text"
```

### Integration Tests

```python
def test_language_selector():
    from app.i18n.language_selector import LanguageSelector
    
    selector = LanguageSelector()
    assert selector.language_combo.count() > 0
    
    # Test language change
    selector.language_combo.setCurrentIndex(1)
    selector._apply_language()
```

## Future Enhancements

- **More Languages**: Add support for additional languages
- **Translation Memory**: Cache frequently used translations
- **Online Translation**: Integration with translation services
- **Translation Editor**: GUI for editing translations
- **Context-Aware Translation**: Context-sensitive translations
- **RTL Support**: Right-to-left language support
- **Translation Statistics**: Usage analytics for translations 
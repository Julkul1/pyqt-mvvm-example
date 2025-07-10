import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeManager(QObject):
    """Manages application themes with JSON format support"""
    
    theme_changed = pyqtSignal(str)  # Signal emitted when theme changes
    
    def __init__(self, themes_dir: str = "themes"):
        super().__init__()
        self.themes_dir = Path(themes_dir)
        self.themes_dir.mkdir(exist_ok=True)
        self.current_theme = "default"
        self.themes: Dict[str, Dict[str, Any]] = {}
        self._load_themes()
    
    def _load_themes(self) -> None:
        """Load all available themes from the themes directory"""
        if not self.themes_dir.exists():
            return
            
        for theme_file in self.themes_dir.glob("*.json"):
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                    theme_name = theme_file.stem
                    self.themes[theme_name] = theme_data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading theme {theme_file}: {e}")
    
    def get_theme_names(self) -> list[str]:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_theme(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Get theme data by name"""
        return self.themes.get(theme_name)
    
    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme to the application"""
        if theme_name not in self.themes:
            return False
            
        theme_data = self.themes[theme_name]
        self.current_theme = theme_name
        
        # Apply stylesheet
        stylesheet = self._generate_stylesheet(theme_data)
        QApplication.instance().setStyleSheet(stylesheet)
        
        # Emit signal
        self.theme_changed.emit(theme_name)
        return True
    
    def _generate_stylesheet(self, theme_data: Dict[str, Any]) -> str:
        """Generate Qt stylesheet from theme data"""
        # Load the default stylesheet
        stylesheet_path = Path(__file__).parent / "default_stylesheet.qss"
        if not stylesheet_path.exists():
            return ""
        
        try:
            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
        except IOError:
            return ""
        
        # Replace CSS variables with theme colors
        colors = theme_data.get('colors', {})
        
        # Define CSS variable replacements
        replacements = {
            'var(--background)': colors.get('background', '#f5f5f5'),
            'var(--surface)': colors.get('surface', '#ffffff'),
            'var(--primary)': colors.get('primary', '#0078d4'),
            'var(--primary-hover)': colors.get('primary_hover', '#106ebe'),
            'var(--secondary)': colors.get('secondary', '#f8f9fa'),
            'var(--text)': colors.get('text', '#333333'),
            'var(--text-secondary)': colors.get('text_secondary', '#666666'),
            'var(--border)': colors.get('border', '#e0e0e0'),
            'var(--border-light)': colors.get('border_light', '#d0d0d0'),
            'var(--success)': colors.get('success', '#28a745'),
            'var(--warning)': colors.get('warning', '#ffc107'),
            'var(--error)': colors.get('error', '#dc3545'),
        }
        
        # Apply replacements
        for variable, color in replacements.items():
            stylesheet = stylesheet.replace(variable, color)
        
        return stylesheet
    
    def save_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Save a theme to JSON file"""
        try:
            theme_file = self.themes_dir / f"{theme_name}.json"
            with open(theme_file, 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
            self.themes[theme_name] = theme_data
            return True
        except IOError as e:
            print(f"Error saving theme {theme_name}: {e}")
            return False
    
    def delete_theme(self, theme_name: str) -> bool:
        """Delete a theme file"""
        try:
            theme_file = self.themes_dir / f"{theme_name}.json"
            if theme_file.exists():
                theme_file.unlink()
                if theme_name in self.themes:
                    del self.themes[theme_name]
                return True
            return False
        except IOError as e:
            print(f"Error deleting theme {theme_name}: {e}")
            return False
    
    def get_current_theme(self) -> str:
        """Get the name of the currently applied theme"""
        return self.current_theme 
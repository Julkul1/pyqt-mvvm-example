from typing import Dict, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal

from app.core.interfaces import ILogger, IThemeService
from app.themes.theme_manager import ThemeManager


class ThemeService(QObject, IThemeService):
    """Service for managing application themes"""
    
    theme_changed = pyqtSignal(str)  # Signal when theme changes
    
    def __init__(self, logger: ILogger):
        super().__init__()
        self.logger = logger
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # Apply default theme on startup
        self.apply_theme("default")
    
    def _on_theme_changed(self, theme_name: str) -> None:
        """Handle theme change from theme manager"""
        self.logger.info(f"Theme changed to: {theme_name}")
        self.theme_changed.emit(theme_name)
    
    def get_available_themes(self) -> list[str]:
        """Get list of available theme names"""
        return self.theme_manager.get_theme_names()
    
    def get_current_theme(self) -> str:
        """Get the name of the currently applied theme"""
        return self.theme_manager.get_current_theme()
    
    def get_theme_data(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Get theme data by name"""
        return self.theme_manager.get_theme(theme_name)
    
    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme to the application"""
        self.logger.info(f"Applying theme: {theme_name}")
        success = self.theme_manager.apply_theme(theme_name)
        if success:
            self.logger.info(f"Successfully applied theme: {theme_name}")
        else:
            self.logger.warning(f"Failed to apply theme: {theme_name}")
        return success
    
    def save_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """Save a theme to JSON file"""
        self.logger.info(f"Saving theme: {theme_name}")
        success = self.theme_manager.save_theme(theme_name, theme_data)
        if success:
            self.logger.info(f"Successfully saved theme: {theme_name}")
        else:
            self.logger.error(f"Failed to save theme: {theme_name}")
        return success
    
    def delete_theme(self, theme_name: str) -> bool:
        """Delete a theme file"""
        self.logger.info(f"Deleting theme: {theme_name}")
        success = self.theme_manager.delete_theme(theme_name)
        if success:
            self.logger.info(f"Successfully deleted theme: {theme_name}")
        else:
            self.logger.error(f"Failed to delete theme: {theme_name}")
        return success
    
    def create_custom_theme(self, name: str, description: str, colors: Dict[str, str]) -> bool:
        """Create a custom theme with basic color scheme"""
        theme_data = {
            "name": name,
            "description": description,
            "colors": {
                "background": colors.get("background", "#f5f5f5"),
                "surface": colors.get("surface", "#ffffff"),
                "primary": colors.get("primary", "#0078d4"),
                "primary_hover": colors.get("primary_hover", "#106ebe"),
                "secondary": colors.get("secondary", "#f8f9fa"),
                "text": colors.get("text", "#333333"),
                "text_secondary": colors.get("text_secondary", "#666666"),
                "border": colors.get("border", "#e0e0e0"),
                "border_light": colors.get("border_light", "#d0d0d0"),
                "success": colors.get("success", "#28a745"),
                "warning": colors.get("warning", "#ffc107"),
                "error": colors.get("error", "#dc3545")
            }
        }
        
        return self.save_theme(name, theme_data) 
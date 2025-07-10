from typing import List, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, pyqtProperty

from app.core.interfaces import ILogger
from app.services.theme_service import ThemeService


class ThemeViewModel(QObject):
    """View model for theme management"""
    
    themes_changed = pyqtSignal()
    current_theme_changed = pyqtSignal()
    
    def __init__(self, theme_service: ThemeService, logger: ILogger):
        super().__init__()
        self._theme_service = theme_service
        self._logger = logger
        
        # Connect to theme service signals
        self._theme_service.theme_changed.connect(self._on_theme_changed)
    
    def _on_theme_changed(self, theme_name: str) -> None:
        """Handle theme change from service"""
        self.current_theme_changed.emit()
    
    @pyqtProperty(list, notify=themes_changed)
    def available_themes(self) -> List[str]:
        """Get list of available theme names"""
        return self._theme_service.get_available_themes()
    
    @pyqtProperty(str, notify=current_theme_changed)
    def current_theme(self) -> str:
        """Get current theme name"""
        return self._theme_service.get_current_theme()
    
    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme"""
        self._logger.info(f"Applying theme: {theme_name}")
        return self._theme_service.apply_theme(theme_name)
    
    def get_theme_info(self, theme_name: str) -> Dict[str, Any]:
        """Get theme information"""
        theme_data = self._theme_service.get_theme_data(theme_name)
        if theme_data:
            return {
                "name": theme_data.get("name", theme_name),
                "description": theme_data.get("description", ""),
                "colors": self._extract_colors(theme_data)
            }
        return {}
    
    def _extract_colors(self, theme_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract color information from theme data"""
        colors = theme_data.get("colors", {})
        
        # Return all available colors
        return {
            "background": colors.get("background", ""),
            "surface": colors.get("surface", ""),
            "primary": colors.get("primary", ""),
            "primary_hover": colors.get("primary_hover", ""),
            "secondary": colors.get("secondary", ""),
            "text": colors.get("text", ""),
            "text_secondary": colors.get("text_secondary", ""),
            "border": colors.get("border", ""),
            "border_light": colors.get("border_light", ""),
            "success": colors.get("success", ""),
            "warning": colors.get("warning", ""),
            "error": colors.get("error", "")
        }
    
    def create_theme(self, name: str, description: str, colors: Dict[str, str]) -> bool:
        """Create a new theme"""
        self._logger.info(f"Creating new theme: {name}")
        success = self._theme_service.create_custom_theme(name, description, colors)
        if success:
            self.themes_changed.emit()
        return success
    
    def delete_theme(self, theme_name: str) -> bool:
        """Delete a theme"""
        if theme_name == "default":
            self._logger.warning("Cannot delete default theme")
            return False
        
        self._logger.info(f"Deleting theme: {theme_name}")
        success = self._theme_service.delete_theme(theme_name)
        if success:
            self.themes_changed.emit()
            # If we deleted the current theme, switch to default
            if theme_name == self.current_theme:
                self.apply_theme("default")
        return success 
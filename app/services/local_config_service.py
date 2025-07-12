import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from app.core.interfaces import IConfigurationService, ILogger


class LocalConfigService(IConfigurationService):
    """Local file-based configuration service for self-contained applications"""
    
    def __init__(self, logger: ILogger, config_file: str = "app_config.json"):
        self._logger = logger
        self._config_file = Path(config_file)
        self._config: Dict[str, Any] = {}
        self._defaults = {
            "app_name": "PyQt MVVM Example",
            "window_width": 1200,
            "window_height": 800,
            "theme": "default",
            "auto_save": True,
            "log_level": "INFO",
            "recent_files": [],
            "user_preferences": {
                "show_toolbar": True,
                "show_statusbar": True,
                "auto_backup": True
            }
        }
        self.load()
    
    def get(self, key: str, default=None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self._config[key] = value
        self._logger.debug(f"Configuration set: {key} = {value}")
    
    def load(self) -> None:
        """Load configuration from local file"""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._config = {**self._defaults, **loaded_config}
                self._logger.info(f"Configuration loaded from {self._config_file}")
            else:
                self._config = self._defaults.copy()
                self._logger.info("Configuration file not found, using defaults")
                self.save()  # Create the file with defaults
        except Exception as e:
            self._logger.error(f"Failed to load configuration: {e}")
            self._config = self._defaults.copy()
    
    def save(self) -> None:
        """Save configuration to local file"""
        try:
            # Ensure directory exists
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            self._logger.info(f"Configuration saved to {self._config_file}")
        except Exception as e:
            self._logger.error(f"Failed to save configuration: {e}")
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values"""
        self._config = self._defaults.copy()
        self.save()
        self._logger.info("Configuration reset to defaults")
    
    def get_user_preference(self, key: str, default=None) -> Any:
        """Get a user preference value"""
        return self._config.get("user_preferences", {}).get(key, default)
    
    def set_user_preference(self, key: str, value: Any) -> None:
        """Set a user preference value"""
        if "user_preferences" not in self._config:
            self._config["user_preferences"] = {}
        self._config["user_preferences"][key] = value
        self._logger.debug(f"User preference set: {key} = {value}")
    
    def add_recent_file(self, file_path: str) -> None:
        """Add a file to recent files list"""
        recent_files = self._config.get("recent_files", [])
        if file_path in recent_files:
            recent_files.remove(file_path)
        recent_files.insert(0, file_path)
        # Keep only last 10 files
        self._config["recent_files"] = recent_files[:10]
        self._logger.debug(f"Added to recent files: {file_path}")
    
    def get_recent_files(self) -> list[str]:
        """Get list of recent files"""
        return self._config.get("recent_files", []) 
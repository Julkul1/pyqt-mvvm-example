import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from app.core.interfaces import IConfigurationService, ILogger


class ConfigurationService(IConfigurationService):
    """Configuration service implementation"""
    
    def __init__(self, logger: ILogger, config_file: str = "config.json"):
        self._logger = logger
        self._config_file = Path(config_file)
        self._config: Dict[str, Any] = {}
        self.load()
    
    def get(self, key: str, default=None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self._config[key] = value
        self._logger.debug(f"Configuration set: {key} = {value}")
    
    def load(self) -> None:
        """Load configuration from file"""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                self._logger.info(f"Configuration loaded from {self._config_file}")
            else:
                self._logger.info("Configuration file not found, using defaults")
                self._set_defaults()
        except Exception as e:
            self._logger.error(f"Failed to load configuration: {e}")
            self._set_defaults()
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            # Ensure directory exists
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            self._logger.info(f"Configuration saved to {self._config_file}")
        except Exception as e:
            self._logger.error(f"Failed to save configuration: {e}")
    
    def _set_defaults(self) -> None:
        """Set default configuration values"""
        self._config = {
            "app_name": "PyQt MVVM Example",
            "window_width": 800,
            "window_height": 600,
            "theme": "default",
            "auto_save": True,
            "log_level": "INFO"
        } 
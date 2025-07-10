import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.interfaces import IDataService, ILogger


class DataService(IDataService):
    """Data persistence service implementation"""
    
    def __init__(self, logger: ILogger, data_file: str = "app_data.json"):
        self._logger = logger
        self._data_file = Path(data_file)
        self._data: Dict[str, Any] = {}
        self._load_data()
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """Save data to file"""
        try:
            # Merge with existing data
            self._data.update(data)
            
            # Ensure directory exists
            self._data_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self._data_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            
            self._logger.info(f"Data saved to {self._data_file}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to save data: {e}")
            return False
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from file"""
        return self._data.copy()
    
    def delete_data(self, key: str) -> bool:
        """Delete a specific data key"""
        try:
            if key in self._data:
                del self._data[key]
                self.save_data({})  # Save the updated data
                self._logger.info(f"Data key '{key}' deleted")
                return True
            else:
                self._logger.warning(f"Data key '{key}' not found")
                return False
        except Exception as e:
            self._logger.error(f"Failed to delete data key '{key}': {e}")
            return False
    
    def get_data(self, key: str, default=None) -> Any:
        """Get a specific data value"""
        return self._data.get(key, default)
    
    def set_data(self, key: str, value: Any) -> bool:
        """Set a specific data value"""
        try:
            self._data[key] = value
            self.save_data({})  # Save the updated data
            return True
        except Exception as e:
            self._logger.error(f"Failed to set data key '{key}': {e}")
            return False
    
    def _load_data(self) -> None:
        """Load data from file on initialization"""
        try:
            if self._data_file.exists():
                with open(self._data_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                self._logger.info(f"Data loaded from {self._data_file}")
            else:
                self._logger.info("Data file not found, starting with empty data")
                self._data = {}
        except Exception as e:
            self._logger.error(f"Failed to load data: {e}")
            self._data = {} 
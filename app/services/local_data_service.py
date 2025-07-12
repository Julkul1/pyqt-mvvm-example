import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.interfaces import IDataService, ILogger


class LocalDataService(IDataService):
    """Local file-based data persistence service for self-contained applications"""
    
    def __init__(self, logger: ILogger, data_dir: str = "data"):
        self._logger = logger
        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(exist_ok=True)
        self._cache: Dict[str, Any] = {}
        self._logger.info(f"Local data service initialized with directory: {self._data_dir}")
    
    def save_data(self, data: Dict[str, Any], filename: str = "app_data.json") -> bool:
        """Save data to local file"""
        try:
            file_path = self._data_dir / filename
            
            # Merge with existing data if file exists
            existing_data = {}
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Update with new data
            existing_data.update(data)
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            # Update cache
            self._cache.update(data)
            
            self._logger.info(f"Data saved to {file_path}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to save data: {e}")
            return False
    
    def load_data(self, filename: str = "app_data.json") -> Dict[str, Any]:
        """Load data from local file"""
        try:
            file_path = self._data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._cache.update(data)
                    self._logger.info(f"Data loaded from {file_path}")
                    return data
            else:
                self._logger.info(f"Data file {file_path} not found")
                return {}
        except Exception as e:
            self._logger.error(f"Failed to load data: {e}")
            return {}
    
    def delete_data(self, key: str, filename: str = "app_data.json") -> bool:
        """Delete a specific data key"""
        try:
            file_path = self._data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if key in data:
                    del data[key]
                    del self._cache[key]
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    self._logger.info(f"Data key '{key}' deleted")
                    return True
                else:
                    self._logger.warning(f"Data key '{key}' not found")
                    return False
            else:
                self._logger.warning(f"Data file {file_path} not found")
                return False
        except Exception as e:
            self._logger.error(f"Failed to delete data key '{key}': {e}")
            return False
    
    def get_data(self, key: str, default=None, filename: str = "app_data.json") -> Any:
        """Get a specific data value"""
        # Check cache first
        if key in self._cache:
            return self._cache[key]
        
        # Load from file if not in cache
        try:
            file_path = self._data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._cache.update(data)
                    return data.get(key, default)
        except Exception as e:
            self._logger.error(f"Failed to get data key '{key}': {e}")
        
        return default
    
    def set_data(self, key: str, value: Any, filename: str = "app_data.json") -> bool:
        """Set a specific data value"""
        try:
            file_path = self._data_dir / filename
            
            # Load existing data
            data = {}
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Update data
            data[key] = value
            self._cache[key] = value
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self._logger.debug(f"Data key '{key}' set to {value}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to set data key '{key}': {e}")
            return False
    
    def save_fuzzy_system(self, system_data: Dict[str, Any], system_name: str) -> bool:
        """Save a fuzzy system to a dedicated file"""
        filename = f"fuzzy_system_{system_name.replace(' ', '_').lower()}.json"
        return self.save_data(system_data, filename)
    
    def load_fuzzy_system(self, system_name: str) -> Dict[str, Any]:
        """Load a fuzzy system from a dedicated file"""
        filename = f"fuzzy_system_{system_name.replace(' ', '_').lower()}.json"
        return self.load_data(filename)
    
    def list_saved_systems(self) -> list[str]:
        """List all saved fuzzy system files"""
        try:
            systems = []
            for file_path in self._data_dir.glob("fuzzy_system_*.json"):
                system_name = file_path.stem.replace("fuzzy_system_", "").replace("_", " ")
                systems.append(system_name)
            return systems
        except Exception as e:
            self._logger.error(f"Failed to list saved systems: {e}")
            return []
    
    def backup_data(self, backup_name: Optional[str] = None) -> bool:
        """Create a backup of all data files"""
        try:
            if backup_name is None:
                from datetime import datetime
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_dir = self._data_dir / "backups" / backup_name
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all data files to backup
            for file_path in self._data_dir.glob("*.json"):
                if file_path.name != "backup":
                    import shutil
                    shutil.copy2(file_path, backup_dir / file_path.name)
            
            self._logger.info(f"Data backup created: {backup_dir}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to create backup: {e}")
            return False 
from typing import Protocol, runtime_checkable

# Note: Using Protocol-based interfaces instead of ABCs to avoid metaclass conflicts with PyQt6


@runtime_checkable
class ILogger(Protocol):
    """Interface for logging service"""
    
    def debug(self, message: str) -> None:
        ...
    
    def info(self, message: str) -> None:
        ...
    
    def warning(self, message: str) -> None:
        ...
    
    def error(self, message: str) -> None:
        ...


@runtime_checkable
class IConfigurationService(Protocol):
    """Interface for configuration service"""
    
    def get(self, key: str, default=None):
        ...
    
    def set(self, key: str, value) -> None:
        ...
    
    def load(self) -> None:
        ...
    
    def save(self) -> None:
        ...


@runtime_checkable
class IDataService(Protocol):
    """Interface for data persistence service"""
    
    def save_data(self, data: dict) -> bool:
        ...
    
    def load_data(self) -> dict:
        ...
    
    def delete_data(self, key: str) -> bool:
        ...
    
    def get_data(self, key: str, default=None):
        ...
    
    def set_data(self, key: str, value) -> bool:
        ... 
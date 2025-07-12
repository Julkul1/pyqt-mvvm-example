from datetime import datetime
from typing import Optional
from app.core.interfaces import ILogger


class ConsoleLoggerService(ILogger):
    """Simple console-based logging service for self-contained applications"""
    
    def __init__(self, name: str = "PyQtMVVM", enabled: bool = True):
        self.name = name
        self.enabled = enabled
        self._log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3
        }
        self._current_level = self._log_levels['INFO']  # Default to INFO level
    
    def set_level(self, level: str) -> None:
        """Set the logging level"""
        if level.upper() in self._log_levels:
            self._current_level = self._log_levels[level.upper()]
    
    def _should_log(self, level: str) -> bool:
        """Check if message should be logged based on current level"""
        return self.enabled and self._log_levels.get(level.upper(), 0) >= self._current_level
    
    def _format_message(self, level: str, message: str) -> str:
        """Format log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {level.upper()}: {self.name} - {message}"
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        if self._should_log('DEBUG'):
            print(self._format_message('DEBUG', message))
    
    def info(self, message: str) -> None:
        """Log info message"""
        if self._should_log('INFO'):
            print(self._format_message('INFO', message))
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        if self._should_log('WARNING'):
            print(self._format_message('WARNING', message))
    
    def error(self, message: str) -> None:
        """Log error message"""
        if self._should_log('ERROR'):
            print(self._format_message('ERROR', message))
    
    def disable(self) -> None:
        """Disable logging"""
        self.enabled = False
    
    def enable(self) -> None:
        """Enable logging"""
        self.enabled = True 
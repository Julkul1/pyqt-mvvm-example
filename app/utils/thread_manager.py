from typing import Callable, Optional, Any
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from app.core.interfaces import ILogger


class ThreadManager(QObject):
    """Manages background threads for the application"""
    
    task_completed = pyqtSignal(object)  # Signal when task completes
    task_error = pyqtSignal(str)  # Signal when task fails
    
    def __init__(self, logger: Optional[ILogger] = None):
        super().__init__()
        self._logger = logger
        self._threads = {}
    
    def run_task(self, task_id: str, task_func, *args, **kwargs):
        """Run a task in a background thread"""
        if task_id in self._threads:
            if self._logger:
                self._logger.warning(f"Task {task_id} is already running")
            return False
        
        # Create worker thread
        thread = QThread()
        worker = TaskWorker(task_func, *args, **kwargs)
        worker.moveToThread(thread)
        
        # Connect signals
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        worker.result.connect(self._on_task_completed)
        worker.error.connect(self._on_task_error)
        
        # Store thread reference
        self._threads[task_id] = thread
        
        # Start thread
        thread.start()
        
        if self._logger:
            self._logger.info(f"Started background task: {task_id}")
        
        return True
    
    def stop_task(self, task_id: str):
        """Stop a running task"""
        if task_id not in self._threads:
            return False
        
        thread = self._threads[task_id]
        thread.quit()
        thread.wait()
        del self._threads[task_id]
        
        if self._logger:
            self._logger.info(f"Stopped background task: {task_id}")
        
        return True
    
    def stop_all_tasks(self):
        """Stop all running tasks"""
        for task_id in list(self._threads.keys()):
            self.stop_task(task_id)
    
    def is_task_running(self, task_id: str) -> bool:
        """Check if a task is currently running"""
        return task_id in self._threads
    
    def get_running_tasks(self) -> list[str]:
        """Get list of currently running task IDs"""
        return list(self._threads.keys())
    
    def _on_task_completed(self, result):
        """Handle task completion"""
        self.task_completed.emit(result)
    
    def _on_task_error(self, error_msg):
        """Handle task error"""
        if self._logger:
            self._logger.error(f"Background task error: {error_msg}")
        self.task_error.emit(error_msg)


class TaskWorker(QObject):
    """Worker object for background tasks"""
    
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Execute the task"""
        try:
            result = self.task_func(*self.args, **self.kwargs)
            self.result.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit() 
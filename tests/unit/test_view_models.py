import pytest
from PyQt6.QtCore import QObject
from app.view_models.counter_view_model import CounterViewModel
from app.models.counter_model import CounterModel


class TestCounterViewModel:
    """Unit tests for CounterViewModel"""
    
    def test_counter_view_model_initialization(self, logger, data_service):
        """Test counter view model initialization"""
        model = CounterModel(logger, data_service)
        view_model = CounterViewModel(model, logger)
        
        assert view_model._model is not None
        assert view_model._logger is not None
        assert view_model._thread_manager is not None
        assert view_model._can_increment is True
        assert view_model._can_decrement is True
    
    def test_counter_view_model_signals(self, logger, data_service):
        """Test that signals are properly defined"""
        model = CounterModel(logger, data_service)
        view_model = CounterViewModel(model, logger)
        
        # Check that signals exist
        assert hasattr(view_model, 'count_changed')
        assert hasattr(view_model, 'can_increment_changed')
        assert hasattr(view_model, 'can_decrement_changed')
        assert hasattr(view_model, 'error_occurred')
    
    def test_counter_view_model_reset(self, logger, data_service):
        """Test reset functionality"""
        model = CounterModel(logger, data_service)
        view_model = CounterViewModel(model, logger)
        
        # Set up a count
        model.increment()
        model.increment()
        assert model.count == 2
        
        # Reset
        view_model.reset()
        
        assert model.count == 0
    
    def test_counter_view_model_button_states(self, logger, data_service):
        """Test button state logic"""
        model = CounterModel(logger, data_service)
        view_model = CounterViewModel(model, logger)
        
        # Initially should be able to increment and decrement
        assert view_model._can_increment is True
        assert view_model._can_decrement is True
        
        # After incrementing to 10, should not be able to increment
        for _ in range(10):
            model.increment()
        
        view_model._update_button_states()
        assert view_model._can_increment is False
        assert view_model._can_decrement is True
        
        # After resetting to 0, should not be able to decrement
        model.reset()
        view_model._update_button_states()
        assert view_model._can_increment is True
        assert view_model._can_decrement is False 
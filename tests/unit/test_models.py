import pytest
from app.models.counter_model import CounterModel


class TestCounterModel:
    """Unit tests for CounterModel"""
    
    def test_counter_model_initialization(self, logger, data_service):
        """Test counter model initialization"""
        model = CounterModel(logger, data_service)
        assert model.count == 0
        assert model._logger is not None
        assert model._data_service is not None
    
    def test_counter_model_increment(self, logger, data_service):
        """Test counter increment functionality"""
        model = CounterModel(logger, data_service)
        initial_count = model.count
        
        model.increment()
        
        assert model.count == initial_count + 1
    
    def test_counter_model_decrement(self, logger, data_service):
        """Test counter decrement functionality"""
        model = CounterModel(logger, data_service)
        model.increment()  # Set to 1
        initial_count = model.count
        
        model.decrement()
        
        assert model.count == initial_count - 1
    
    def test_counter_model_decrement_below_zero(self, logger, data_service):
        """Test that decrement doesn't go below zero"""
        model = CounterModel(logger, data_service)
        assert model.count == 0
        
        model.decrement()
        
        assert model.count == 0  # Should remain at 0
    
    def test_counter_model_reset(self, logger, data_service):
        """Test counter reset functionality"""
        model = CounterModel(logger, data_service)
        model.increment()
        model.increment()
        assert model.count == 2
        
        model.reset()
        
        assert model.count == 0
    
    def test_counter_model_get_count(self, logger, data_service):
        """Test get_count method"""
        model = CounterModel(logger, data_service)
        model.increment()
        model.increment()
        
        count = model.get_count()
        
        assert count == 2 
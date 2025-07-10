import pytest
import json
from pathlib import Path
from app.services.logger_service import LoggerService
from app.services.configuration_service import ConfigurationService
from app.services.data_service import DataService


class TestLoggerService:
    """Unit tests for LoggerService"""
    
    def test_logger_service_initialization(self):
        """Test logger service initialization"""
        logger = LoggerService("TestLogger")
        assert logger.logger is not None
        assert logger.logger.name == "TestLogger"
    
    def test_logger_service_methods(self):
        """Test logger service methods"""
        logger = LoggerService("TestLogger")
        
        # These should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")


class TestConfigurationService:
    """Unit tests for ConfigurationService"""
    
    def test_configuration_service_initialization(self, logger, temp_dir):
        """Test configuration service initialization"""
        config_file = temp_dir / "test_config.json"
        config_service = ConfigurationService(logger, str(config_file))
        
        assert config_service._logger is not None
        assert config_service._config_file == config_file
    
    def test_configuration_service_get_set(self, logger, temp_dir):
        """Test configuration get and set methods"""
        config_file = temp_dir / "test_config.json"
        config_service = ConfigurationService(logger, str(config_file))
        
        # Test set and get
        config_service.set("test_key", "test_value")
        value = config_service.get("test_key")
        assert value == "test_value"
        
        # Test default value
        default_value = config_service.get("non_existent_key", "default")
        assert default_value == "default"
    
    def test_configuration_service_save_load(self, logger, temp_dir):
        """Test configuration save and load"""
        config_file = temp_dir / "test_config.json"
        config_service = ConfigurationService(logger, str(config_file))
        
        # Set some values
        config_service.set("key1", "value1")
        config_service.set("key2", "value2")
        
        # Save
        config_service.save()
        
        # Create new instance to test load
        new_config_service = ConfigurationService(logger, str(config_file))
        
        # Check values were loaded
        assert new_config_service.get("key1") == "value1"
        assert new_config_service.get("key2") == "value2"


class TestDataService:
    """Unit tests for DataService"""
    
    def test_data_service_initialization(self, logger, temp_dir):
        """Test data service initialization"""
        data_file = temp_dir / "test_data.json"
        data_service = DataService(logger, str(data_file))
        
        assert data_service._logger is not None
        assert data_service._data_file == data_file
    
    def test_data_service_save_load_data(self, logger, temp_dir):
        """Test data service save and load"""
        data_file = temp_dir / "test_data.json"
        data_service = DataService(logger, str(data_file))
        
        test_data = {"key1": "value1", "key2": "value2"}
        
        # Save data
        success = data_service.save_data(test_data)
        assert success is True
        
        # Load data
        loaded_data = data_service.load_data()
        assert loaded_data["key1"] == "value1"
        assert loaded_data["key2"] == "value2"
    
    def test_data_service_get_set_data(self, logger, temp_dir):
        """Test data service get and set individual values"""
        data_file = temp_dir / "test_data.json"
        data_service = DataService(logger, str(data_file))
        
        # Set individual values
        data_service.set_data("user_id", 123)
        data_service.set_data("username", "test_user")
        
        # Get individual values
        user_id = data_service.get_data("user_id")
        username = data_service.get_data("username")
        
        assert user_id == 123
        assert username == "test_user"
        
        # Test default value
        default_value = data_service.get_data("non_existent", "default")
        assert default_value == "default"
    
    def test_data_service_delete_data(self, logger, temp_dir):
        """Test data service delete functionality"""
        data_file = temp_dir / "test_data.json"
        data_service = DataService(logger, str(data_file))
        
        # Set some data
        data_service.set_data("key1", "value1")
        data_service.set_data("key2", "value2")
        
        # Delete one key
        success = data_service.delete_data("key1")
        assert success is True
        
        # Check key1 is gone
        value = data_service.get_data("key1")
        assert value is None
        
        # Check key2 still exists
        value = data_service.get_data("key2")
        assert value == "value2" 
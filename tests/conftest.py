import pytest
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

from app.services.logger_service import LoggerService
from app.services.configuration_service import ConfigurationService
from app.services.data_service import DataService
from app.services.fuzzy_logic_service import FuzzyLogicService
from app.services.theme_service import ThemeService


@pytest.fixture
def logger():
    """Provide a logger service for tests"""
    return LoggerService()


@pytest.fixture
def config_service(logger):
    """Provide a configuration service for tests"""
    return ConfigurationService(logger)


@pytest.fixture
def data_service(logger):
    """Provide a data service for tests"""
    return DataService(logger)


@pytest.fixture
def fuzzy_logic_service(logger):
    """Provide a fuzzy logic service for tests"""
    return FuzzyLogicService(logger)


@pytest.fixture
def theme_service(logger):
    """Provide a theme service for tests"""
    return ThemeService(logger)


@pytest.fixture
def services(logger, config_service, data_service, fuzzy_logic_service, theme_service):
    """Provide all services for tests"""
    return {
        'logger': logger,
        'config_service': config_service,
        'data_service': data_service,
        'fuzzy_logic_service': fuzzy_logic_service,
        'theme_service': theme_service
    }


@pytest.fixture(scope="function")
def temp_dir(tmp_path):
    """Create a temporary directory for test files"""
    return tmp_path


@pytest.fixture(scope="function")
def sample_data():
    """Sample data for testing"""
    return {
        "counter_count": 5,
        "user_preferences": {
            "theme": "dark",
            "language": "en"
        },
        "test_list": ["item1", "item2", "item3"]
    } 
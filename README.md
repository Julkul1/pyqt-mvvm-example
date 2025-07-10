# 🚀 PyQt MVVM Professional Application

A comprehensive PyQt6 application demonstrating advanced MVVM architecture with enterprise-grade features including dependency injection, event-driven communication, comprehensive testing, and professional project structure.

## ✨ Features

### 🏗️ **Advanced Architecture**
- **MVVM Pattern**: Clean separation of concerns
- **Dependency Injection**: Loose coupling with service container
- **Repository Pattern**: Abstract data access layer
- **Event System**: Decoupled communication between components
- **Thread Management**: Generalized background task handling

### 🛠️ **Professional Development Tools**
- **Comprehensive Testing**: Unit, integration, and UI tests
- **Code Quality**: Linting, formatting, and type checking
- **Documentation**: Auto-generated API docs and guides
- **Build System**: Automated build and deployment
- **CI/CD Ready**: GitHub Actions workflows

### 🎨 **Modern UI/UX**
- **Theme System**: Light and dark themes
- **Responsive Design**: Adaptive layouts
- **Custom Components**: Reusable UI widgets
- **Accessibility**: Screen reader support

### 🔧 **Enterprise Features**
- **Configuration Management**: Environment-specific settings
- **Logging System**: Structured logging with rotation
- **Validation Framework**: Data integrity and validation
- **Caching System**: Performance optimization
- **Security**: Authentication and authorization ready

## 📁 Project Structure

```
pyqt-mvvm-example/
├── app/                          # Main application code
│   ├── core/                     # Core architecture
│   │   ├── interfaces.py         # Abstract base classes
│   │   ├── container.py          # Dependency injection
│   │   ├── service_locator.py    # Service access
│   │   ├── events/               # Event system
│   │   └── validation/           # Validation framework
│   ├── di/                       # Dependency injection
│   │   └── services/             # Service interfaces & implementations
│   ├── models/                   # Data models
│   ├── view_models/              # View models
│   ├── views/                    # UI components
│   │   ├── counter/              # Feature-based organization
│   │   └── main/
│   ├── services/                 # Business services
│   ├── repositories/             # Data access layer
│   └── utils/                    # Utilities
├── tests/                        # Comprehensive test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── ui/                       # UI tests
├── config/                       # Configuration management
│   ├── environments/             # Environment-specific configs
│   └── themes/                   # UI themes
├── build/                        # Build and deployment
│   └── scripts/                  # Build scripts
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   ├── user_guide/               # User documentation
│   ├── developer_guide/          # Developer documentation
│   └── architecture/             # Architecture documentation
└── scripts/                      # Development scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PyQt6

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pyqt-mvvm-example.git
   cd pyqt-mvvm-example
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Types
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# UI tests
pytest tests/ui/ -v
```

### Code Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Development

### Code Quality
```bash
# Linting
flake8 app/ tests/

# Formatting
black app/ tests/

# Type checking
mypy app/
```

### Build Application
```bash
# Build distribution
python build/scripts/build.py

# Build executable
python build/scripts/build.py --exe
```

### Documentation
```bash
# Generate API docs
sphinx-build docs/source docs/build/html

# View documentation
open docs/build/html/index.html
```

## 📚 Documentation

- **[User Guide](docs/user_guide/)** - How to use the application
- **[Developer Guide](docs/developer_guide/)** - Development setup and guidelines
- **[API Documentation](docs/api/)** - Code reference
- **[Architecture](docs/architecture/)** - System design and patterns

## 🏗️ Architecture Overview

### MVVM Pattern
```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│    View     │◄──►│   ViewModel     │◄──►│    Model    │
│   (UI)      │    │ (Presentation)  │    │  (Data)     │
└─────────────┘    └─────────────────┘    └─────────────┘
```

### Dependency Injection
```python
# Service registration
container.register_singleton(ILogger, LoggerService)
container.register_singleton(IDataService, DataService)

# Dependency resolution
logger = ServiceLocator.get_service(ILogger)
model = CounterModel(logger, data_service)
```

### Event System
```python
# Subscribe to events
event_bus.subscribe("data_changed", self.handle_data_change)

# Publish events
event_bus.publish("data_changed", new_data)
```

## 🎯 Key Features Explained

### 1. **Thread Management**
Generalized background task handling with proper cleanup:
```python
# Execute any function in background
self._thread_manager.execute_task(self._model.heavy_operation)

# Handle completion and errors
self._thread_manager.task_finished.connect(self._on_complete)
self._thread_manager.task_error.connect(self._on_error)
```

### 2. **Repository Pattern**
Abstract data access with multiple implementations:
```python
# Interface
class ICounterRepository(IBaseRepository[CounterModel]):
    def get_current_count(self) -> int: ...

# Implementation
class FileCounterRepository(ICounterRepository):
    def get_current_count(self) -> int:
        return self._data_service.get_data("counter_count", 0)
```

### 3. **Validation Framework**
Comprehensive data validation:
```python
# Create validation rules
engine.add_rule("user", ValidationRule("email", [RequiredValidator(), EmailValidator()]))

# Validate data
errors = engine.validate("user", {"email": "invalid-email"})
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow the MVVM pattern
- Write comprehensive tests
- Update documentation
- Follow code style guidelines
- Use dependency injection

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyQt6 team for the excellent framework
- MVVM pattern pioneers
- Open source community for inspiration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/pyqt-mvvm-example/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pyqt-mvvm-example/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/pyqt-mvvm-example/wiki)

---

**Built with ❤️ using PyQt6 and MVVM architecture**
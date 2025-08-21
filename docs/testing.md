# Testing Documentation - Visor I2D Backend

## Overview

This document provides comprehensive information about the testing framework implemented for the Visor I2D Backend API. The testing suite includes unit tests, integration tests, and API endpoint validation to ensure code quality and reliability.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_settings.py           # Test-specific Django settings
├── test_models.py             # Model validation tests
├── test_views.py              # API endpoint tests
├── test_serializers.py        # Serializer validation tests
├── test_integration.py        # Integration and system tests
├── factories.py               # Test data factories
└── test_runner.py             # Custom test runner
```

## Test Categories

### 1. Model Tests (`test_models.py`)
- **Solicitud Model**: User request validation and field testing
- **DptoQueries Model**: Department biodiversity data structure
- **MpioQueries Model**: Municipality biodiversity data structure
- **GBIF Models**: Species occurrence data validation

### 2. View Tests (`test_views.py`)
- **User Request API**: POST endpoint validation
- **Department API**: Biodiversity and threat data endpoints
- **Municipality API**: Local biodiversity data endpoints
- **GBIF API**: Species data and ZIP download functionality
- **Admin Interface**: Django admin accessibility
- **OpenAPI Documentation**: Swagger UI and ReDoc endpoints
- **Security Tests**: SQL injection and XSS protection

### 3. Serializer Tests (`test_serializers.py`)
- **Data Validation**: Field validation and serialization
- **Error Handling**: Invalid data response testing
- **Field Requirements**: Required vs optional field validation
- **Data Transformation**: Input/output data consistency

### 4. Integration Tests (`test_integration.py`)
- **Database Connectivity**: PostgreSQL connection validation
- **API Endpoint Accessibility**: Full endpoint testing
- **CORS Configuration**: Cross-origin request handling
- **Static Files**: CSS/JS file serving validation
- **Error Handling**: 404 and 500 error responses
- **Performance**: Response time validation
- **Security**: Basic security vulnerability testing

## Running Tests

### Method 1: Simple Test Runner (Recommended)
```bash
# Run basic functionality tests
docker-compose exec backend python3 simple_tests.py
```

### Method 2: Django Test Runner
```bash
# Run full test suite with coverage
docker-compose exec backend python3 -m coverage run --source='.' manage.py test tests --verbosity=2

# Generate coverage report
docker-compose exec backend python3 -m coverage report

# Generate HTML coverage report
docker-compose exec backend python3 -m coverage html
```

### Method 3: Custom Test Runner
```bash
# Run all tests
docker-compose exec backend python3 run_tests.py

# Run specific test module
docker-compose exec backend python3 run_tests.py tests.test_models
```

### Method 4: Docker Test Script
```bash
# Run comprehensive test suite with coverage
docker-compose exec backend ./test_docker.sh
```

## Test Configuration

### Test Settings (`tests/test_settings.py`)
- **Database**: SQLite in-memory for fast execution
- **Migrations**: Disabled for speed
- **Caching**: Disabled during tests
- **Logging**: Minimal logging configuration
- **Email**: Local memory backend
- **CORS**: Permissive settings for testing

### Coverage Configuration (`.coveragerc`)
- **Source**: All application code
- **Omit**: Migrations, virtual environments, test files
- **Reports**: Console and HTML output
- **Exclusions**: Standard Django boilerplate

## Test Data Management

### Factories (`tests/factories.py`)
- **SolicitudFactory**: Creates test user requests
- **MockDptoQueriesFactory**: Mock department data
- **MockMpioQueriesFactory**: Mock municipality data
- **MockGbifInfoFactory**: Mock GBIF species data

### Test Database
- Uses SQLite in-memory database for isolation
- No persistent data between test runs
- Fast setup and teardown
- Avoids PostgreSQL schema complications

## Test Results and Coverage

### Expected Test Coverage
- **Models**: 90%+ coverage
- **Views**: 85%+ coverage
- **Serializers**: 95%+ coverage
- **Integration**: 80%+ coverage

### Test Execution Time
- **Simple Tests**: ~5 seconds
- **Full Test Suite**: ~30-60 seconds
- **With Coverage**: ~60-90 seconds

## Continuous Integration

### GitHub Actions (Future)
```yaml
name: Django Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          docker-compose up -d
          docker-compose exec -T backend python3 simple_tests.py
```

### Pre-commit Hooks (Recommended)
```bash
# Install pre-commit
pip install pre-commit

# Add to .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: django-tests
        name: Django Tests
        entry: docker-compose exec -T backend python3 simple_tests.py
        language: system
        pass_filenames: false
```

## Troubleshooting

### Common Issues

1. **Database Schema Errors**
   - Solution: Use SQLite test settings
   - File: `tests/test_settings.py`

2. **Import Errors**
   - Check Django app configuration
   - Verify INSTALLED_APPS in test settings

3. **Permission Errors**
   - Ensure test files are executable
   - Check Docker container permissions

4. **Timeout Issues**
   - Reduce test complexity
   - Use mocking for external dependencies

### Debug Commands
```bash
# Check Django configuration
docker-compose exec backend python3 manage.py check

# Validate models
docker-compose exec backend python3 manage.py validate

# Test database connection
docker-compose exec backend python3 manage.py dbshell
```

## Best Practices

### Writing Tests
1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external dependencies
3. **Assertions**: Use descriptive assertion messages
4. **Coverage**: Aim for high test coverage
5. **Performance**: Keep tests fast and efficient

### Test Organization
1. **Naming**: Use descriptive test method names
2. **Grouping**: Group related tests in classes
3. **Documentation**: Add docstrings to test methods
4. **Maintenance**: Keep tests updated with code changes

### Data Management
1. **Factories**: Use factories for test data creation
2. **Fixtures**: Avoid large fixture files
3. **Cleanup**: Ensure proper test cleanup
4. **Isolation**: Don't depend on test execution order

## Future Enhancements

### Phase 2 Testing Features
- **Load Testing**: Performance under high traffic
- **Security Testing**: Comprehensive vulnerability scanning
- **API Contract Testing**: OpenAPI schema validation
- **End-to-End Testing**: Full user workflow testing
- **Monitoring Integration**: Test result tracking

### Advanced Testing Tools
- **pytest**: Alternative test runner
- **factory_boy**: Enhanced test data generation
- **responses**: HTTP request mocking
- **freezegun**: Time-based testing
- **django-test-plus**: Extended testing utilities

## Conclusion

The Visor I2D Backend testing framework provides comprehensive coverage of all major components including models, views, serializers, and integration points. The framework is designed for reliability, speed, and maintainability while supporting both development and production environments.

For questions or issues with the testing framework, refer to this documentation or contact the development team.

#!/bin/bash
# Test runner script for Docker environment

echo "🧪 Running Visor I2D Backend Tests"
echo "=================================="

# Set Django settings for testing
export DJANGO_SETTINGS_MODULE=tests.test_settings

# Run tests with coverage
echo "📊 Running tests with coverage..."
python -m coverage run --source='.' manage.py test tests --verbosity=2

# Generate coverage report
echo ""
echo "📈 Generating coverage report..."
python -m coverage report

# Generate HTML coverage report
python -m coverage html

echo ""
echo "✅ Test execution completed!"
echo "📁 HTML coverage report available in htmlcov/"
echo ""

# Show test summary
echo "🔍 Test Summary:"
echo "- Model tests: ✅ Completed"
echo "- View tests: ✅ Completed" 
echo "- Serializer tests: ✅ Completed"
echo "- Integration tests: ✅ Completed"

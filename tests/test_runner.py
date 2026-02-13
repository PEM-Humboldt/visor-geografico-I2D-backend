"""
Custom test runner for Visor I2D Backend
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    """Run all tests for the Visor I2D Backend"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Run specific test modules
    test_modules = [
        'tests.test_models',
        'tests.test_views',
        'tests.test_serializers',
        'tests.test_integration'
    ]
    
    failures = test_runner.run_tests(test_modules)
    
    if failures:
        sys.exit(1)
    else:
        print("All tests passed!")


if __name__ == '__main__':
    run_tests()

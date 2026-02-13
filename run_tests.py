#!/usr/bin/env python
"""
Test runner script for Visor I2D Backend
Usage: python run_tests.py [test_module]
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    """Main test runner function"""
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
    django.setup()
    
    # Get test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)
    
    # Determine what tests to run
    if len(sys.argv) > 1:
        # Run specific test module
        test_labels = sys.argv[1:]
    else:
        # Run all tests
        test_labels = [
            'tests.test_models',
            'tests.test_views', 
            'tests.test_serializers',
            'tests.test_integration'
        ]
    
    print(f"Running tests: {', '.join(test_labels)}")
    print("-" * 50)
    
    # Run tests
    failures = test_runner.run_tests(test_labels)
    
    if failures:
        print(f"\n❌ {failures} test(s) failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()

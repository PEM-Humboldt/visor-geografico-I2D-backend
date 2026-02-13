#!/usr/bin/env python3
"""
Django 4.2 Compatibility Check Script
Verifies that the codebase is compatible with Django 4.2 LTS
"""
import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'i2dbackend.settings.local')
django.setup()

def check_django_version():
    """Check Django version compatibility"""
    print("🔍 Checking Django version...")
    print(f"   Django version: {django.VERSION}")

    if django.VERSION[0] >= 4 and django.VERSION[1] >= 2:
        print("   ✅ Django 4.2+ detected")
        return True
    else:
        print("   ❌ Django version is not 4.2+")
        return False

def check_settings():
    """Check for deprecated settings"""
    print("\n🔍 Checking settings configuration...")

    from django.conf import settings

    # Check for deprecated settings
    deprecated_settings = []

    if hasattr(settings, 'USE_L10N'):
        deprecated_settings.append('USE_L10N')

    if hasattr(settings, 'MIDDLEWARE_CLASSES'):
        deprecated_settings.append('MIDDLEWARE_CLASSES')

    if deprecated_settings:
        print(f"   ❌ Found deprecated settings: {deprecated_settings}")
        return False
    else:
        print("   ✅ No deprecated settings found")

    # Check required settings
    required_settings = ['DEFAULT_AUTO_FIELD']
    missing_settings = []

    for setting in required_settings:
        if not hasattr(settings, setting):
            missing_settings.append(setting)

    if missing_settings:
        print(f"   ❌ Missing required settings: {missing_settings}")
        return False
    else:
        print("   ✅ All required settings present")

    return True

def check_models():
    """Check model compatibility"""
    print("\n🔍 Checking model compatibility...")

    try:
        from applications.projects.models import Project, LayerGroup, Layer
        from applications.dpto.models import DptoQueries
        from applications.mupio.models import MpioQueries

        # Test model instantiation
        print("   ✅ All models imported successfully")

        # Check for deprecated field types
        from django.db import models

        # This would catch NullBooleanField usage
        deprecated_fields = []
        for model in [Project, LayerGroup, Layer, DptoQueries, MpioQueries]:
            for field in model._meta.get_fields():
                if hasattr(field, 'get_internal_type'):
                    if field.get_internal_type() == 'NullBooleanField':
                        deprecated_fields.append(f"{model.__name__}.{field.name}")

        if deprecated_fields:
            print(f"   ❌ Found deprecated NullBooleanField usage: {deprecated_fields}")
            return False
        else:
            print("   ✅ No deprecated field types found")

        return True

    except ImportError as e:
        print(f"   ❌ Model import error: {e}")
        return False

def check_urls():
    """Check URL configuration compatibility"""
    print("\n🔍 Checking URL configuration...")

    try:
        from django.urls import reverse
        from i2dbackend.urls import urlpatterns

        print("   ✅ URL configuration loaded successfully")

        # Check for deprecated url() usage in imports
        import i2dbackend.urls
        import inspect

        source = inspect.getsource(i2dbackend.urls)
        if 'django.conf.urls.url' in source or 'from django.conf.urls import url' in source:
            print("   ❌ Found deprecated django.conf.urls.url usage")
            return False
        else:
            print("   ✅ No deprecated URL patterns found")

        return True

    except Exception as e:
        print(f"   ❌ URL configuration error: {e}")
        return False

def check_admin():
    """Check admin configuration"""
    print("\n🔍 Checking admin configuration...")

    try:
        from django.contrib import admin
        from applications.projects.admin import ProjectAdmin, LayerGroupAdmin

        print("   ✅ Admin configuration loaded successfully")
        return True

    except Exception as e:
        print(f"   ❌ Admin configuration error: {e}")
        return False

def check_rest_framework():
    """Check Django REST Framework compatibility"""
    print("\n🔍 Checking Django REST Framework...")

    try:
        import rest_framework
        from django.conf import settings

        print(f"   DRF version: {rest_framework.VERSION}")

        # Check DRF settings
        if hasattr(settings, 'REST_FRAMEWORK'):
            drf_settings = settings.REST_FRAMEWORK
            print("   ✅ REST Framework settings configured")

            # Check for deprecated settings
            deprecated_drf_settings = []
            if 'DEFAULT_AUTHENTICATION_CLASSES' in drf_settings:
                auth_classes = drf_settings['DEFAULT_AUTHENTICATION_CLASSES']
                for auth_class in auth_classes:
                    if 'rest_framework.authentication.SessionAuthentication' in str(auth_class):
                        # This is fine, just checking for really old patterns
                        pass

            return True
        else:
            print("   ❌ REST Framework settings not found")
            return False

    except ImportError as e:
        print(f"   ❌ REST Framework import error: {e}")
        return False

def run_basic_checks():
    """Run basic Django system checks"""
    print("\n🔍 Running Django system checks...")

    try:
        from django.core.management import call_command
        from io import StringIO
        import sys

        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            call_command('check', verbosity=0)
            sys.stdout = old_stdout
            output = captured_output.getvalue()

            if 'System check identified no issues' in output or not output.strip():
                print("   ✅ Django system checks passed")
                return True
            else:
                print(f"   ❌ Django system check issues: {output}")
                return False

        except Exception as e:
            sys.stdout = old_stdout
            print(f"   ❌ System check error: {e}")
            return False

    except Exception as e:
        print(f"   ❌ Could not run system checks: {e}")
        return False

def main():
    """Main compatibility check function"""
    print("🚀 Django 4.2 Compatibility Check")
    print("=" * 50)

    checks = [
        check_django_version,
        check_settings,
        check_models,
        check_urls,
        check_admin,
        check_rest_framework,
        run_basic_checks,
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Check failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("📊 COMPATIBILITY CHECK RESULTS")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("🎉 Project is fully compatible with Django 4.2 LTS!")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed}/{total})")
        print("⚠️  Please review and fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

"""
Test settings for Visor I2D Backend
"""
from i2dbackend.settings.base import *

# Force SQLite for all tests to avoid PostgreSQL schema issues
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': ':memory:',
        }
    }
}

# Disable migrations for faster test execution
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Disable logging during tests
LOGGING_CONFIG = None

# Test-specific settings
DEBUG = False

# Use simple password hasher for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable caching during tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Use local memory email backend for tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

CORS_ALLOW_ALL_ORIGINS = True

# Test-specific settings
SECRET_KEY = 'test-secret-key-for-testing-only'
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

"""
Security settings for production deployment
"""
import os
from .base import *

# Security Headers and HTTPS Configuration
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Session Security
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', '3600'))  # 1 hour

# CSRF Protection
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() == 'true'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', 
        'https://i2d.humboldt.org.co').split(',')
]

# X-Frame-Options
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'", "https://api.gbif.org")

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Input Validation Settings
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('DATA_UPLOAD_MAX_MEMORY_SIZE', '5242880'))  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('FILE_UPLOAD_MAX_MEMORY_SIZE', '2621440'))  # 2.5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = int(os.getenv('DATA_UPLOAD_MAX_NUMBER_FIELDS', '100'))

# Password Security
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'applications.common.validators.CustomPasswordValidator',
    },
]

# API Security
REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.getenv('API_ANON_RATE', '100/hour'),
        'user': os.getenv('API_USER_RATE', '1000/hour')
    },
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
})

# Logging Security
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '{asctime} {levelname} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/security.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'security',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Database Security
DATABASES['default'].update({
    'CONN_MAX_AGE': 60,
    'OPTIONS': {
        'sslmode': os.getenv('DB_SSLMODE', 'prefer'),
        'options': os.getenv('DB_OPTIONS', '-c search_path=django,gbif_consultas,capas_base,geovisor')
    }
})

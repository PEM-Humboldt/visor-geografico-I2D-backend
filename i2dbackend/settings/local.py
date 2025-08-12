from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

# ALLOWED_HOSTS configuration
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '0.0.0.0,localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',')]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),

        'OPTIONS': {
            'options': os.getenv('DB_OPTIONS', '-c search_path=django,gbif_consultas,capas_base,geovisor')
        },

        'NAME': os.getenv('DB_NAME', get_secret('DB_NAME')),

        'USER': os.getenv('DB_USER', get_secret('USER')),

        'PASSWORD': os.getenv('DB_PASSWORD', get_secret('PASSWORD')),

        'HOST': os.getenv('DB_HOST', get_secret('HOST')),

        'PORT': os.getenv('DB_PORT', get_secret('PORT'))

    }
}

# Static files configuration
STATIC_ROOT = os.getenv('STATIC_ROOT', '/app/static')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/media')


# CORS settings
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS',
        'https://i2d.humboldt.org.co,http://i2d.humboldt.org.co/visor-I2D/,localhost:1234,0.0.0.0:1234').split(',')
]

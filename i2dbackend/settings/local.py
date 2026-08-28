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

        'ENGINE': os.getenv('DB_ENGINE', 'django.contrib.gis.db.backends.postgis'),

        'OPTIONS': {
            'options': os.getenv('DB_OPTIONS', '-c search_path=django,gbif_consultas,capas_base,geovisor')
        },

        'NAME': os.getenv('DB_NAME') or get_secret('DB_NAME'),

        'USER': os.getenv('DB_USER') or get_secret('USER'),

        'PASSWORD': os.getenv('DB_PASSWORD') or get_secret('PASSWORD'),

        'HOST': os.getenv('DB_HOST') or get_secret('HOST')

    }
}

# Static files configuration
STATIC_ROOT = os.getenv('STATIC_ROOT', '/app/static')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/media')

# S3 bucket configuration
S3_ENDPOINT_URL= os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'visors3')
S3_AUTH_TOKEN = os.getenv('S3_AUTH_TOKEN')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
S3_DEFAULT_REGION = os.getenv('S3_DEFAULT_REGION', 'sa-east-1')

# CORS settings
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://(localhost|127\.0\.0\.1)(:\d+)?$",
]

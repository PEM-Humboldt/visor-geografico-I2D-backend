from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'false').lower() == 'false'

# ALLOWED_HOSTS configuration
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', 'web,localhost')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',')]

# Database configuration using environment variables
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.contrib.gis.db.backends.postgis'),
        'OPTIONS': {
            'options': os.getenv('DB_OPTIONS', '-c search_path=django,gbif_consultas,capas_base,geovisor')
        },
        'NAME': os.getenv('DB_NAME') or get_secret('DB_NAME'),
        'USER': os.getenv('DB_USER') or get_secret('USER'),
        'PASSWORD': os.getenv('DB_PASSWORD') or get_secret('PASSWORD'),
        'HOST': os.getenv('DB_HOST') or get_secret('HOST'),
        'PORT': os.getenv('DB_PORT') or get_secret('PORT'),
    }
}

# Sub-path bajo el que la app es expuesta por el reverse proxy / ALB.
# Ej: si la app se accede en https://host/visor-I2D/api/, definir
# FORCE_SCRIPT_NAME=/visor-I2D/api en el entorno. None = sin prefix.
FORCE_SCRIPT_NAME = os.getenv('FORCE_SCRIPT_NAME') or None
USE_X_FORWARDED_HOST = True

# El ALB termina TLS y reenvía como HTTP al backend. Sin esto, Django
# genera redirects http:// que rompen el flujo (login del admin, etc.).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static / media files configuration
STATIC_ROOT = os.getenv('STATIC_ROOT', '/app/static')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/media')

_url_prefix = (FORCE_SCRIPT_NAME or '').rstrip('/')
STATIC_URL = f'{_url_prefix}/static/'
MEDIA_URL = f'{_url_prefix}/media/'

# S3 bucket configuration
S3_ENDPOINT_URL= os.getenv('S3_ENDPOINT_URL')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'visors3')
S3_AUTH_TOKEN = os.getenv('S3_AUTH_TOKEN')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
S3_DEFAULT_REGION = os.getenv('S3_DEFAULT_REGION', 'sa-east-1')

# CORS settings
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS',
        'https://i2d.humboldt.org.co,http://i2d.humboldt.org.co').split(',')
]

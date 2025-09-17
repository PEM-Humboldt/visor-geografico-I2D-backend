from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Secrets file is optional; environment variables are the source of truth.
# You can override the path via SECRET_FILE env var. Default points to project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SECRET_FILE = os.environ.get('SECRET_FILE', os.path.join(PROJECT_ROOT, 'secret.json'))

def _load_secrets(path):
    try:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return {}
    except Exception as e:
        # If an explicit path was provided and it's unreadable, fail fast
        if os.environ.get('SECRET_FILE'):
            raise ImproperlyConfigured(f"Error leyendo el archivo de secretos en {path}: {e}")
        return {}

secret = _load_secrets(SECRET_FILE)

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except KeyError:
        msg = "la variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)

# Read SECRET_KEY from environment first, then from optional secrets file.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or secret.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY no está definido y no existe SECRET_KEY en el archivo de secretos"
    )

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

LOCAL_APPS = (
    'applications.dpto',
    'applications.mupio',
    'applications.mupiopolitico',
    'applications.gbif',
    'applications.user',
    'applications.projects',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'corsheaders',
    'drf_yasg',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'applications.common.middleware.SecurityHeadersMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'applications.common.middleware.RequestLoggingMiddleware',
    'applications.common.middleware.DataQualityMiddleware',
    'applications.common.middleware.APIVersioningMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'applications.common.middleware.ErrorHandlingMiddleware',
]

ROOT_URLCONF = 'i2dbackend.urls'

# cada parent indica cuantas carpetas escalar arriba
BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'i2dbackend.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Django 4.2+ required setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# DRF YASG Settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
    'OPERATIONS_SORTER': 'alpha',
    'TAGS_SORTER': 'alpha',
    'DOC_EXPANSION': 'none',
    'DEEP_LINKING': True,
    'SHOW_EXTENSIONS': True,
    'SHOW_COMMON_EXTENSIONS': True,
}


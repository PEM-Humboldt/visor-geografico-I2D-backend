from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['web','localhost']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'OPTIONS': {
            'options': '-c search_path=django,gbif_consultas,capas_base'
        },

        'NAME': get_secret('DB_NAME'),

        'USER': get_secret('USER'),

        'PASSWORD': get_secret('PASSWORD'),

        'HOST': get_secret('HOST'),

        'PORT': get_secret('PORT'),

    }
}

CORS_ALLOWED_ORIGINS = [
    "https://i2d.humboldt.org.co",
    "http://i2d.humboldt.org.co/visor-I2D/",
    #"http://localhost:8080",
    #"http://127.0.0.1:9000"
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

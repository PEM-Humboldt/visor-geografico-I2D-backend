from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ec2-54-197-164-22.compute-1.amazonaws.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'OPTIONS': {
            'options': '-c search_path=django,gbif'
        },

        'NAME': get_secret('DB_NAME'),

        'USER': get_secret('USER'),

        'PASSWORD': get_secret('PASSWORD'),

        'HOST': get_secret('HOST'),

        'PORT': get_secret('PORT')

    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

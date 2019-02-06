from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'var/db.sqlite3',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

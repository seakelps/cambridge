import os.path
import dj_database_url
import django_heroku
from .settings import *

DEBUG = True

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

# sending emails
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SSL/HTTPS and other security-related settings
ALLOWED_HOSTS = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

django_heroku.settings(
    locals(),
    databases=True,
    staticfiles=True,
    test_runner=False,
    logging=False,
)

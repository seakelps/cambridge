import os.path
import dj_database_url
import django_heroku
from .settings import *

DEBUG = False

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))
ADMINS = [(email, email) for email in os.getenv('DJANGO_ADMINS', '').split() if email]

# TODO: This is a hack while waiting for
if os.environ.get('CI'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'HerokuCI'
    }

# sending emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.privateemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@cambridge.vote'
DEFAULT_FROM_EMAIL = 'admin@cambridge.vote'
EMAIL_HOST_PASSWORD = os.environ.get('PRIVATEEMAIL_ADMIN_PASS')
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SSL/HTTPS and other security-related settings
ALLOWED_HOSTS = ['.cambridgecouncilcandidates.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# MIDDLEWARE += [
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ]

django_heroku.settings(locals())

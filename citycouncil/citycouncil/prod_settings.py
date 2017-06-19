import os.path
import dj_database_url
from .settings import *

DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

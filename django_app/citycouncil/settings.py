import os
import dj_database_url
import datetime


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ["DJANGO_DEBUG"] == "TRUE"

# Allow Django to detect that the original request was https so build absolute url picks https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOST"].split(",")
CSRF_TRUSTED_ORIGINS = [
    "https://cambridge-wh2u.onrender.com",
    "https://www.cambridge-wh2u.onrender.com",
    "https://cambridge.vote",
    "https://www.cambridge.vote",

    # old urls, to be removed after 2025
    "https://cambridgecouncilcandidates.com",
    "https://www.cambridgecouncilcandidates.com",
]
ATOMIC_REQUESTS = True

FIXTURE_DIRS = [os.path.join(BASE_DIR, "fixtures")]

ELECTION_DATE = datetime.date(2025, 11, 4)


# Application definition

INSTALLED_APPS = [
    # ours
    "overview",
    "voting_history",
    "campaign_finance",
    "ranking",
    # others
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "fullurl",
    "crispy_forms",
    "crispy_bootstrap4",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"


SITE_ID = 1


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
]

ROOT_URLCONF = "citycouncil.urls"
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]


class InvalidString(str):
    def __mod__(self, other):
        from django.template.base import TemplateSyntaxError

        raise TemplateSyntaxError('Undefined variable or unknown value for: "%s"' % other)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "string_if_invalid": InvalidString("%s"),
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "overview.context_processors.header",
                "overview.context_processors.constants",
                "ranking.context_processors.sidebar",
            ],
        },
    },
]

WSGI_APPLICATION = "citycouncil.wsgi.application"


DATABASES = {
    "default": dj_database_url.parse(
        os.environ["DJANGO_DATABASE_URL"],
        conn_max_age=600,
        conn_health_checks=True,
    ),
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage" 
            if DEBUG else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    },
}


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "static_compiled"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("DJANGO_MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
CONTACT_EMAIL = "admin@cambridge.vote"

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# this is only for dev; production is configured differently.
# that said, production's configurations work in dev, so you can test them
# by commenting out EMAIL_BACKEND and copying all the production email settings.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
GOOGLE_EMBED_API_KEY = os.getenv("GOOGLE_EMBED_API_KEY")

import logging
import os
from pathlib import Path

import dj_database_url
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env()


BASE_DIR = Path(__file__).resolve().parent.parent

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    filename=BASE_DIR / "logs.events.log",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    datefmt="%H:%M:%S",
    style="{",
)
# Mute debug logging for faker library used in tests
logging.getLogger("faker").setLevel(logging.ERROR)


DEBUG = env.bool("DJANGO_DEBUG", default=False)

if DEBUG:
    SECRET_KEY = env("DJANGO_SECRET_KEY", default="wow-so-secret")
    ALLOWED_HOSTS = ["*"]
else:
    SECRET_KEY = env("DJANGO_SECRET_KEY")
    ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")


# HTTPS / SSL settings
# if os.getenv("LETSENCRYPT_HOST", None):
#     SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # disable Django’s static file handling and allow WhiteNoise to take over
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "task_manager.apps.TaskManagerConfig",
    "bootstrap4",
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_manager.wsgi.application"

# Authentication

AUTH_USER_MODEL = "task_manager.SiteUser"

LOGIN_REDIRECT_URL = "index"

LOGOUT_REDIRECT_URL = "index"

LOGIN_URL = "login"

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    },
}

SQLITE_SETTINGS = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

if os.getenv("DB_ENGINE") == "SQLite":
    DATABASES["default"] = SQLITE_SETTINGS


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CONN_MAX_AGE = 500

# Use the DATABASE_URL environment variable
# https://pypi.org/project/dj-database-url/
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(conn_max_age=CONN_MAX_AGE)


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# Internationalization
LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files
STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Project specific settings
PROJECT_NAME = "Task Manager"


# Settings for django-bootstrap4
BOOTSTRAP4 = {
    "error_css_class": "bootstrap4-error",
    "required_css_class": "bootstrap4-required",
    "javascript_in_head": True,
    "include_jquery": True,
    "theme_url": "https://getbootstrap.com/docs/4.5/examples/navbar-fixed/navbar-top-fixed.css",
}

# crispy_forms template settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

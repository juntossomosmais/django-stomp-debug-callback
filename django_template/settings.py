import os

from distutils.util import strtobool
from logging import Formatter
from pathlib import Path
from typing import List
from typing import Optional

from pythonjsonlogger.jsonlogger import JsonFormatter

from django_template.apps.example.apps import ExampleConfig

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "False"))

DJANGO_ALLOWED_HOSTS: Optional[str] = os.getenv("ALLOWED_HOSTS")
if DJANGO_ALLOWED_HOSTS:
    EXTRA_ALLOWED_HOST: Optional[str] = os.getenv("EXTRA_ALLOWED_HOST")
    FINAL_ALLOWED_HOSTS = f"{DJANGO_ALLOWED_HOSTS},{EXTRA_ALLOWED_HOST}" if EXTRA_ALLOWED_HOST else DJANGO_ALLOWED_HOSTS
    ALLOWED_HOSTS = FINAL_ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = ["*"]


CSRF_COOKIE_SECURE = strtobool(os.getenv("CSRF_COOKIE_SECURE", "True"))
SESSION_COOKIE_SECURE = strtobool(os.getenv("SESSION_COOKIE_SECURE", "True"))


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "request_id_django_log",
    "health_check",
    "health_check.db",
    "autodynatrace.wrappers.django",
]

LOCAL_APPS: List[str] = [
    "django_template.apps.example",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django_template.support.middleware.LivenessHealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_template.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "django_template.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 20)),
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (),
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASE_SSL_MODE = os.getenv("DB_SSL_MODE")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

DATABASES["default"]["CONN_MAX_AGE"] = int(os.getenv("DB_CONN_MAX_AGE", 0))  # type: ignore

if DATABASE_SSL_MODE:
    DATABASES["default"]["OPTIONS"].update({"sslmode": DATABASE_SSL_MODE})  # type: ignore

if strtobool(os.getenv("USE_REPLICA", "False")):
    DATABASES["replica"] = {
        "ENGINE": os.getenv("DB_ENGINE_REPLICA"),
        "NAME": os.getenv("DB_DATABASE_REPLICA"),
        "USER": os.getenv("DB_USER_REPLICA"),
        "HOST": os.getenv("DB_HOST_REPLICA"),
        "PORT": os.getenv("DB_PORT_REPLICA"),
        "PASSWORD": os.getenv("DB_PASSWORD_REPLICA"),
    }

    DATABASES["replica"]["CONN_MAX_AGE"] = int(os.getenv("DB_CONN_MAX_AGE", 0))  # type: ignore

    DATABASE_ROUTERS: List[str] = []  # Place your database router path here

    if DATABASE_SSL_MODE:
        DATABASES["replica"]["OPTIONS"].update({"sslmode": DATABASE_SSL_MODE})  # type: ignore

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "request_id_django_log.filters.RequestIDFilter"},
        "redact_filter": {
            "()": "django_template.support.logger.RedactingFilter",
            "patterns": ["cpf", "email", "birthday", "gender", "number", "emails", "username", "name", "phone"],
        },
    },
    "formatters": {
        "standard": {
            "()": JsonFormatter,
            "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] [%(session_id)s] %(name)s: %(message)s",
        },
        "development": {
            "()": Formatter,
            "format": "%(asctime)s - request-id=%(request_id)s - level=%(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id", "redact_filter"],
            "formatter": os.getenv("DEFAULT_LOG_FORMATTER", "standard"),
        }
    },
    "loggers": {
        "": {"level": os.getenv("ROOT_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django_template": {
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {"level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "handlers": ["console"]},
        "django.db.backends": {"level": os.getenv("DJANGO_DB_BACKENDS_LOG_LEVEL", "INFO"), "handlers": ["console"]},
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
USE_STATIC_FILE_HANDLER_FROM_WSGI = strtobool(os.getenv("USE_STATIC_FILE_HANDLER_FROM_WSGI", "true"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###############################
# Custom settings

# Liveness URL
LIVENESS_URL = os.getenv("LIVENESS_URL", "/healthcheck/liveness")

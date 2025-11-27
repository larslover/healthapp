from pathlib import Path
import os
from dotenv import load_dotenv

# ---------------------
# Load environment variables
# ---------------------
load_dotenv()  # reads .env file if present

# ---------------------
# Paths
# ---------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # adjust for your project layout

# ---------------------
# Security
# ---------------------
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")  # replace with strong key in prod
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "larslover.pythonanywhere.com").split(",")

# ---------------------
# Installed apps
# ---------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",  # your app
]

# ---------------------
# Middleware
# ---------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------
# URLs & WSGI
# ---------------------
ROOT_URLCONF = "healthapp.urls"
WSGI_APPLICATION = "healthapp.wsgi.application"

# ---------------------
# Templates
# ---------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # optional
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

# ---------------------
# Database
# ---------------------
# Leave DATABASES config to production.py / dev.py
# This base.py doesn't define database

# ---------------------
# Password validators
# ---------------------
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

# ---------------------
# Internationalization
# ---------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------
# Static files
# ---------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # optional for dev
STATIC_ROOT = BASE_DIR / "staticfiles"    # used in collectstatic

# ---------------------
# Media files
# ---------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------
# Default primary key field type
# ---------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

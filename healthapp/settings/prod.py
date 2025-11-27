from .base import *
import os

# ---------------------
# Debug
# ---------------------
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# ---------------------
# Secret Key
# ---------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")  # fallback if .env missing

# ---------------------
# Database (MySQL on PythonAnywhere)
# ---------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "LarsLover$healthapp"),
        "USER": os.getenv("DB_USER", "LarsLover"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "LarsLover.mysql.pythonanywhere-services.com"),
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ---------------------
# Security
# ---------------------
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ---------------------
# Allowed Hosts
# ---------------------
# ---------------------
# Allowed Hosts
# ---------------------
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]


# ---------------------
# Static & Media
# ---------------------
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

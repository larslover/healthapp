from .base import *
import os

# ---------------------
# Debug
# ---------------------
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# ---------------------
# Database (MySQL on PythonAnywhere)
# ---------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "LarsLover$healthapp"),
        "USER": os.environ.get("DB_USER", "LarsLover"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "LarsLover.mysql.pythonanywhere-services.com"),
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

# HSTS (high security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ---------------------
# Allowed Hosts
# ---------------------
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "larslover.pythonanywhere.com").split(",")

# ---------------------
# Static & Media
# ---------------------
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

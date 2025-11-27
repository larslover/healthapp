from .base import *

# ---------------------
# Debug
# ---------------------
DEBUG = False

# ---------------------
# Secret Key
# ---------------------
SECRET_KEY = "l-mxo2jss+^w$_@z%02@$4zgkt79ye-7f04u(=+9h()k08p2-^"  # use your generated key

# ---------------------
# Database (MySQL on PythonAnywhere)
# ---------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "LarsLover$healthapp",
        "USER": "LarsLover",
        "PASSWORD": "Lars1978",
        "HOST": "LarsLover.mysql.pythonanywhere-services.com",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ---------------------
# Security & Allowed Hosts
# ---------------------
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

ALLOWED_HOSTS = ["gahealthapp.com", "www.gahealthapp.com", "larslover.pythonanywhere.com"]

# ---------------------
# Static & Media
# ---------------------
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

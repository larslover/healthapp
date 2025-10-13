from .base import *

DEBUG = os.getenv('DEBUG', 'True') == 'True'
DATABASE_ROUTERS = ['db_router.DBRouter']


# SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gracehealth_mock.db',  # new, clean app DB
    },
    'legacy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'client_data.db',  # old client DB
    }
}

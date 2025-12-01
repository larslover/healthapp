from .base import *

DEBUG = os.getenv('DEBUG', 'True') == 'True'
DATABASE_ROUTERS = ['db_router.DBRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev_gracehealth.db',   # <- empty DB where Django writes
    },
    'legacy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gracehealth.db',       # <- real client DB
    }
}

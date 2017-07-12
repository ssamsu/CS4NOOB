from .settings import *

# Creating in-memory SQLite DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# This will stop sending the actual memory as we will be keeping it in local memory
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

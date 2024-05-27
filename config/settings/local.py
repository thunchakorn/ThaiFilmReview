from .base import *


SECRET_KEY = "django-insecure-(1mo=!yrwopz)w(3ckyjl*i41&#=0su!v@lrp_up%02^ntz58o"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

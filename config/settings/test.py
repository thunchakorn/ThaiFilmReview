from .base import *
from .base import env


SECRET_KEY = "%_y0fhl97jc(wy1ed!^p_mpk3%b%u0mvw1i428nhzqa^p&f-+"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db",
    }
}

from .base import *
from .base import env


SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="%_y0fhl97jc(wy1ed!^p_mpk3%b%u0mvw1i428nhzqa^p&f-+",
)


DATABASES = {"default": env.db_url("DJANGO_DATABASE_URL")}

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = "mailpit"
EMAIL_PORT = 1025

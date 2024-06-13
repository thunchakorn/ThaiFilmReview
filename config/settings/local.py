from .base import *
from .base import env


SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="%_y0fhl97jc(wy1ed!^p_mpk3%b%u0mvw1i428nhzqa^p&f-+",
)

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}


DATABASES = {"default": env.db_url("DATABASE_URL")}

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = "mailpit"
EMAIL_PORT = 1025

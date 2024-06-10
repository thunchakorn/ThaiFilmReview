import os

from .base import *
from .base import env

# https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOST")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = env.str(
    "DJANGO_EMAIL_HOST_USER", default="thaifilmreviewweb@gmail.com"
)
EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD")

# DATABASE
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db_url("DATABASE_URL")}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage", # need django-storages extension
#         "OPTIONS": {
#         },
#     },
# }

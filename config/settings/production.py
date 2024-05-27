import os

from .base import *

# https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = False
ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.environ["SECRET_KEY"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "thaifilmreviewweb@gmail.com"
EMAIL_HOST_PASSWORD = ""

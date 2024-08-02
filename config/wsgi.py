"""
WSGI config for TFRW project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from config.settings import base

print("base.DEBUG", base.DEBUG)
if base.DEBUG:
    print("use:", "config.settings.local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    print("use:", "config.settings.production")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = get_wsgi_application()

"""
ASGI config for TFRW project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from config.settings import base

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from tfr.routing import websocket_urlpatterns

print("base.DEBUG", base.DEBUG)
if base.DEBUG:
    print("use:", "config.settings.local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    print("use:", "config.settings.production")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

"""
ASGI config for tradex project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradingbackend.settings')

application = get_asgi_application()


# Needed if starting server using daphne or uvicorn command
import django
django.setup()

from channels.auth import AuthMiddlewareStack
from mainapp.routing import websocket_urlpatterns
"""need to add websocket as we are using it and need to add in settings also as channel layer"""
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
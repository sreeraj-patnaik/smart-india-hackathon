"""
ASGI config for sih project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from index import consumers as index_consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sih.settings")

django_asgi_app = get_asgi_application()

websocket_urlpatterns = [
    path("ws/chat/", index_consumers.ChatConsumer.as_asgi()),
    path("ws/forum/", index_consumers.ForumConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})

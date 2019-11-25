from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import routing
from chat import token_auth

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': token_auth(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
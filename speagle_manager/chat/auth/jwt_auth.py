from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from django.conf import settings
from django.contrib.auth import get_user_model

from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from functools import partial


@database_sync_to_async
def get_user(self, scope, decoded_data):
    user = get_user_model().objects.get(id=decoded_data['user_id'])
    return user

class JWTBaseAuthMiddleware():
    def __init__(self, inner):
        """
        Middleware constructor - just takes inner application.
        """
        self.inner = inner

    def __call__(self, scope):
        """
        ASGI constructor; can insert things into the scope, but not
        run asynchronous code.
        """
        scope = dict(scope)
        self.populate_scope(scope)
        inner_instance = self.inner(scope)

        return partial(self.coroutine_call, inner_instance, scope)
    
    async def coroutine_call(self, inner_instance, scope, receive, send):
        """
        ASGI coroutine; where we can resolve items in the scope
        (but you can't modify it at the top level here!)
        """
        await self.resolve_scope(scope, receive, send)
        # await inner_instance(receive, send)


class JWTAuthMiddleware(JWTBaseAuthMiddleware):
    def populate_scope(self, scope):
        if b'token' not in scope['query_string']:
            raise ValueError(
                'JWTMiddleware cannot find token in scope.'
            )

    async def resolve_scope(self, scope, receive, send):
        token = parse_qs(scope['query_string'].decode('utf8'))['token'][0]
        # print('token -> ' + str(token))

        try:
            UntypedToken(token) # Verify JWT
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # print('decoded_data -> ' + str(decoded_data))

            scope['user'] = await get_user(self, scope, decoded_data)
            print('middleware scope -> ' + str(scope))

            inner_instance = self.inner(scope)
            await inner_instance(receive, send)
            
        except (InvalidToken, TokenError) as e:
            print(e)
        
# JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
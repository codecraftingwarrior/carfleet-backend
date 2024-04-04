import collections
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()


class TokenAuthMiddleware(BaseMiddleware):
    token = None

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        self.token = query_string.get('token', None)
        if self.token is not None and isinstance(self.token, collections.abc.Sequence):
            self.token = self.token[0]

        if self.token is None:
            scope['user'] = AnonymousUser()
        else:
            scope['user'] = await self.fetch_user_from_token()
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def fetch_user_from_token(self):
        try:
            untyped_token = UntypedToken(self.token)
            user_id = untyped_token['user_id']

            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist) as e:
            return AnonymousUser()

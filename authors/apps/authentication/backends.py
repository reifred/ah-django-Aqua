import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User
from rest_framework.response import Response

"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        token_type = auth_header[0].decode('utf-8')

        if token_type not in ["Token", "Bearer"]:
            msg = 'Bad Authorization header.'
            raise exceptions.AuthenticationFailed(msg)

        token = auth_header[1].decode('utf-8')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            msg = 'Your token expired. Log In again.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(username=payload['usn'])
        except User.DoesNotExist:
            msg = f"user with username {payload['usn']} is not found"
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'User nolonger has account with us'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)

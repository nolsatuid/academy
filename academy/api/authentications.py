import jwt
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, load_backend, SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from jwt import InvalidTokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.utils.translation import ugettext_lazy as _


class APISessionAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth = request.data.get('session_key') or request.query_params.get('session_key')
        if not auth:
            raise exceptions.AuthenticationFailed("Session key isn't supplied")

        user = self.get_user(auth)
        if user:
            return (user, auth)

        raise exceptions.AuthenticationFailed('Invalid session id')

    def get_user(self, session_key):
        '''
            Get user object from it's cached sessionid
            source : https://djangosnippets.org/snippets/1276/
        '''

        session_engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        session_wrapper = session_engine.SessionStore(session_key)
        session = session_wrapper.load()
        user_id = session.get(SESSION_KEY)
        backend_id = session.get(BACKEND_SESSION_KEY)

        if user_id and backend_id:
            auth_backend = load_backend(backend_id)
            user = auth_backend.get_user(user_id)
            if user:
                return user

        return None


class InternalAPIAuthentication(BaseAuthentication):
    def authenticate(self, request):
        self.validate_token(request)
        return AnonymousUser(), None

    def validate_token(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        if validated_token.get("server_key", None) != settings.SERVER_KEY:
            raise InvalidToken(_('Token contained no recognizable server key'))

        return validated_token

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_AUTHORIZATION')
        #
        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0].decode(HTTP_HEADER_ENCODING) != "Server":
            # Assume the header does not contain a JSON web token
            raise AuthenticationFailed(
                _('Authorization not from server'),
                code='bad_authorization_header',
            )

        if len(parts) != 2:
            raise AuthenticationFailed(
                _('Authorization header must contain two space-delimited values'),
                code='bad_authorization_header',
            )

        return parts[1]

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        try:
            raw_token = raw_token.decode(HTTP_HEADER_ENCODING)
            return jwt.decode(raw_token, settings.SECRET_KEY)
        except InvalidTokenError as e:
            messages.append(str(e))

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })


class InternalAPIMixin:
    authentication_classes = (InternalAPIAuthentication,)


class UserAuthMixin:
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, APISessionAuthentication)


class UserAuthAPIView(UserAuthMixin, APIView):
    pass


class InternalAPIView(InternalAPIMixin, APIView):
    pass

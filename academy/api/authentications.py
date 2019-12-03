from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, load_backend, SESSION_KEY
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


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


class UserAuthAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication, APISessionAuthentication)

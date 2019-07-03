from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from academy.api.authentications import UserAuthAPIView


class GetProfileView(UserAuthAPIView):

    def get(self, request):
        content = {
            'email': request.user.email,
        }
        return Response(content)

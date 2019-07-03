from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from academy.api.authentications import UserAuthAPIView
from academy.api.serializers import user_profile


class GetProfileView(UserAuthAPIView):

    def get(self, request):
        return Response(user_profile(request.user))

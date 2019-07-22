import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from academy.api.authentications import UserAuthAPIView
from academy.api.serializers import user_profile
from academy.api.response import ErrorResponse
from academy.website.accounts.forms import ProfileForm


class GetProfileView(UserAuthAPIView):

    def get(self, request):
        return Response(user_profile(request.user), status=status.HTTP_200_OK)

    def post(self, request):
        if hasattr(request.user, 'profile'):
            form = ProfileForm(
                data=request.data, files=request.FILES, instance=request.user.profile,
                cv_required=False
            )
        else:
            form = ProfileForm(data=request.data, files=request.FILES, cv_required=False)

        if form.is_valid():
            form.save(request.user)
            return Response(user_profile(request.user))
        return ErrorResponse(form)

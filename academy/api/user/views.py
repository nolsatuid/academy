from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from academy.api.authentications import UserAuthAPIView
from academy.api.serializers import user_profile
from academy.website.accounts.forms import ProfileForm


class GetProfileView(UserAuthAPIView):

    def get(self, request):
        return Response(user_profile(request.user))

    def post(self, request):
        form = ProfileForm(data=request.data, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save(request.user)
            return Response(user_profile(request.user))
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

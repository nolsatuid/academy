from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from academy.api.authentications import UserAuthAPIView
from academy.api.response import ErrorResponse
from academy.api.serializers import user_profile
from academy.api.user.forms import UploadCVForm, UploadAvatarForm
from academy.api.user.serializer import SurveySerializer
from academy.website.accounts.forms import ProfileForm, SurveyForm


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


class UploadCV(UserAuthAPIView):
    def post(self, request):
        if hasattr(request.user, 'profile'):
            form = UploadCVForm(files=request.FILES, instance=request.user.profile)
        else:
            form = UploadCVForm(files=request.FILES)

        if form.is_valid():
            form.save()
            return Response(user_profile(request.user))
        return ErrorResponse(form)


class SurveyView(UserAuthAPIView):
    @staticmethod
    def build_response(survey=None):
        return {
            "data": SurveySerializer(survey).data if survey else None
        }

    def get(self, request):
        survey = request.user.survey
        return JsonResponse(self.build_response(survey))

    def post(self, request):
        form = SurveyForm(data=request.data)
        survey = request.user.survey
        if form.is_valid():
            if survey:
                survey.delete()

            form.save(request.user)
            return JsonResponse(self.build_response(request.user.survey))

        return ErrorResponse(form)


class UploadAvatar(UserAuthAPIView):
    def post(self, request):
        print("kesini")
        if hasattr(request.user, 'profile'):
            form = UploadAvatarForm(files=request.FILES, instance=request.user.profile)
        else:
            form = UploadAvatarForm(files=request.FILES)

        if form.is_valid():
            form.save()
            return Response(user_profile(request.user))
        return ErrorResponse(form)

from rest_framework import status
from rest_framework.response import Response

from academy.api.authentications import UserAuthAPIView
from academy.api.response import ErrorResponse
from academy.api.serializers import user_profile, training_material, graduate_data
from academy.api.user.forms import UploadCVForm, UploadAvatarForm
from academy.api.user.serializer import SurveySerializer
from academy.website.accounts.forms import ProfileForm, SurveyForm

from django.contrib.auth.forms import PasswordChangeForm


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


class UploadCVView(UserAuthAPIView):
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
    def build_response(user):
        survey = getattr(user, 'survey', None)
        return {
            "data": SurveySerializer(survey).data if survey else None
        }

    def get(self, request):
        return Response(self.build_response(request.user))

    def post(self, request):
        survey = getattr(request.user, 'survey', None)
        form = SurveyForm(data=request.data, instance=survey)
        if form.is_valid():
            form.save(request.user)
            return Response(self.build_response(request.user))

        return ErrorResponse(form)


class UploadAvatarView(UserAuthAPIView):
    def post(self, request):
        if hasattr(request.user, 'profile'):
            form = UploadAvatarForm(files=request.FILES, instance=request.user.profile)
        else:
            form = UploadAvatarForm(files=request.FILES)

        if form.is_valid():
            form.save()
            return Response(user_profile(request.user))
        return ErrorResponse(form)


class MaterialsView(UserAuthAPIView):
    def get(self, request):
        user = request.user
        student = user.get_student()

        training_materials = student.training.materials.prefetch_related('training_status')
        return Response({
            "data": [
                training_material(materi, user) for materi in training_materials
            ]
        })


class GetGraduateView(UserAuthAPIView):
    def get(self, request):
        student = request.user.get_student()

        if hasattr(student, 'graduate'):
            response = {
                "data": graduate_data(student.graduate)
            }
        else:
            response = {"data": None}

        return Response(response)


class ChangePasswordView(UserAuthAPIView):
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.data or None)

        if form.is_valid():
            form.save()
            return Response({'message': 'Password berhasil diubah'})

        return ErrorResponse(form)

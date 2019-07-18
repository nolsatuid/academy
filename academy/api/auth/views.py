from academy.website.accounts.forms import CustomAuthenticationForm
from academy.api.response import ErrorResponse
from academy.api.serializers import user_profile

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import APIRegisterForm


class AuthLogin(APIView):
    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.data)
        if form.is_valid():
            user = form.get_user()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_profile(user)
            }
            return Response(data)
        return ErrorResponse(form)


class RegisterView(APIView):
    def post(self, request):
        form = APIRegisterForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({'message': f'Mohon cek kotak masuk / spam {user.email} untuk mengaktifkan akun Anda'})

        return ErrorResponse(form)

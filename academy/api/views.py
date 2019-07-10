from rest_framework.response import Response
from rest_framework.views import APIView

from academy.api.response import ErrorResponse
from .forms import APIRegisterForm


class RegisterView(APIView):
    def post(self, request):
        form = APIRegisterForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({'message': f'Mohon cek email {user.email} untuk mengaktifkan akun Anda'})

        return ErrorResponse(form)

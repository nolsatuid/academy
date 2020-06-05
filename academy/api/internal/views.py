from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from academy.api.authentications import InternalAPIView
from academy.api.internal.forms import GenerateCertificateForm
from academy.api.internal.serializers import (
    CertificateSerializer, UserSerializer, AddInboxSerializer
)
from academy.api.response import ErrorResponse
from academy.api.response import ErrorResponse
from academy.apps.accounts.models import User, Certificate


class DemoView(InternalAPIView):
    def get(self, request):
        return Response(data={
            'message': 'Hellow from academy'
        })

    def post(self, request):
        user_id = request.data.get('user_id', None)
        other_info = request.data.get('other_info', None)
        return Response(data={
            'user_id': user_id,
            'other_info': other_info
        })


class GenerateCertificateView(InternalAPIView):
    def post(self, request, *args, **kwargs):
        form = GenerateCertificateForm(data=request.data)
        if form.is_valid():
            certificate = form.save()
            return Response(CertificateSerializer(certificate).data)
        return ErrorResponse(form)


class UserView(InternalAPIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return Response(UserSerializer(user).data)


class SendNotification(InternalAPIView):
    def post(self, request):
        serializer = AddInboxSerializer(data=request.data)
        if serializer.is_valid():
            inbox = serializer.save()
            inbox.send_notification()
            return Response({'message': 'Pesan berhasil disimpan'})

        return ErrorResponse(serializer=serializer)


class RegenerateCertificateView(InternalAPIView):
    def get(self, request, user_id):
        certificates = Certificate.objects.filter(user=user_id)
        if certificates:
            for cert in certificates:
                cert.generate()
            return Response({'message': 'Berhasil generate ulang sertifikat'})

        return ErrorResponse(error_message='Gagal generate ulang sertifikat')


class GetUserView(InternalAPIView):
    def get(self, request):
        email = request.GET.get('email')
        username = request.GET.get('username')
        if email:
            user = get_object_or_404(User, email=email)
        else:
            user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data)

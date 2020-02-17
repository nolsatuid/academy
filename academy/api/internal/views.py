from rest_framework.response import Response

from academy.api.authentications import InternalAPIView
from academy.api.internal.forms import GenerateCertificateForm
from academy.api.internal.serializers import CertificateSerializer
from academy.api.response import ErrorResponse


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

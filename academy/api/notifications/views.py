from rest_framework.response import Response

from academy.api.authentications import UserAuthAPIView
from academy.api.response import ErrorResponse
from academy.apps.accounts.models import Inbox


class SendNotification(UserAuthAPIView):
    def post(self, request):
        data = request.data
        inbox = Inbox.objects.create(user=request.user, subject=data["title"], content=data["content"])

        if inbox :
            return Response({'message': 'Pesan berhasil disimpan'})
        
        return ErrorResponse(error_message='Pesan gagal disimpan')

        
        
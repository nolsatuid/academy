from rest_framework.response import Response

from django.utils.datastructures import MultiValueDictKeyError

from academy.api.authentications import UserAuthAPIView
from academy.api.response import ErrorResponse
from academy.apps.accounts.models import Inbox, User


class SendNotification(UserAuthAPIView):
    def post(self, request):
        data = request.data

        try :
            user = User.objects.get(id=data["user_id"])
        except User.DoesNotExist :
            return ErrorResponse(error_message='User tidak tersedia')

        try :
            inbox = Inbox.objects.create(user=user, subject=data["title"], content=data["content"])
            return Response({'message': 'Pesan berhasil disimpan'})
        except MultiValueDictKeyError:
            return ErrorResponse(error_message='Parameter tidak sesuai')
        
        return ErrorResponse(error_message='Pesan gagal disimpan')

        
        
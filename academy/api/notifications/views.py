from rest_framework.response import Response

from django.utils.datastructures import MultiValueDictKeyError

from academy.api.authentications import UserAuthAPIView
from academy.api.response import ErrorResponse

from .forms import AddInboxForm

class SendNotification(UserAuthAPIView):
    def post(self, request):      
        form = AddInboxForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Pesan berhasil disimpan'})

        return ErrorResponse(form)

        
        
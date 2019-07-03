from rest_framework.response import Response
from rest_framework.views import APIView

from academy.apps.accounts.models import User
from academy.apps.students.models import Student
from academy.apps.graduates.models import Graduate


class GetStatisticsView(APIView):

    def get(self, request):
        context = {
            'registrants': User.objects.registered().count(),
            'users': User.objects.actived().count(),
            'participants': Student.objects.participants().count(),
            'graduates': Student.objects.graduated().count(),
            'channeled': Graduate.objects.filter(is_channeled=True).count(),
        }
        return Response(context)

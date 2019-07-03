from rest_framework.response import Response
from rest_framework.views import APIView

from academy.apps.accounts.models import User
from academy.apps.students.models import Student
from academy.apps.graduates.models import Graduate
from academy.apps.offices.models import LogoPartner, LogoSponsor
from academy.api import serializers


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


class GetLogoPartners(APIView):
    logos = LogoPartner.objects.filter(is_visible=True).order_by('display_order')

    def get(self, request):
        context = [
            serializers.logo(logo) for logo in self.logos
        ]
        return Response(context)


class GetLogoSponsors(GetLogoPartners):
    logos = LogoSponsor.objects.filter(is_visible=True).order_by('display_order')

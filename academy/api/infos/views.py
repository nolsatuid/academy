from datetime import timedelta

from rest_framework.response import Response
from rest_framework.views import APIView

from academy.api.response import ErrorResponse
from academy.apps.accounts.models import User
from academy.apps.students.models import Student
from academy.apps.graduates.models import Graduate
from academy.apps.offices.models import LogoPartner, LogoSponsor
from academy.api import serializers
from academy.website.forms import CertificateVerifyForm


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
        context = {
            "data": [serializers.logo(logo) for logo in self.logos]
        }
        return Response(context)


class GetLogoSponsors(GetLogoPartners):
    logos = LogoSponsor.objects.filter(is_visible=True).order_by('display_order')


class VerifyCertificate(APIView):
    def post(self, request):
        form = CertificateVerifyForm(request.data or None)
        if form.is_valid():
            student = form.verification()
            if student:
                valid_date = student.created + timedelta(days=1095)
                context = {
                    'pemilik': f'{student.user.first_name} {student.user.last_name}',
                    'nomor_sertifikat': student.certificate_number,
                    'tanggal_sertifikat': student.created.strftime('%d %b %Y'),
                    'berlaku_hingga': valid_date.strftime('%d %b %Y')
                }
                return Response(context)

            return ErrorResponse(error_message='Maaf, kami tidak dapat menemukan sertifikat dengan '
                                               'nomor sertifikat dan nama belakang tersebut.')

        return ErrorResponse(form)

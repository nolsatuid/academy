from django.core.management.base import BaseCommand
from academy.apps.graduates.models import Graduate


class Command(BaseCommand):
    help = 'Generate all Certificate'

    def handle(self, *args, **options):

        graduates = Graduate.objects \
            .exclude(certificate_number=None).exclude(certificate_number="")

        for graduate in graduates:
            graduate.generate_certificate_file(force=True)
            print(f"Generate {graduate} certificate is success")

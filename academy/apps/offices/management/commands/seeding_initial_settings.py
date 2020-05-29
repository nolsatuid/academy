from django.core.management.base import BaseCommand
from academy.apps.offices.models import Setting


class Command(BaseCommand):
    help = 'To Seeding Initial Settings data'

    def handle(self, *args, **options):
        Setting.objects.update_or_create(
            name="Apperance",
            defaults={
                'site_name': 'NolSatu',
                'footer_title': 'PT. Boer Technology (Btech)',
                'footer_url': 'https://btech.id/',
            }
        )

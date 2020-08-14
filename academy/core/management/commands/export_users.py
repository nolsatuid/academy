from django.core.management.base import BaseCommand

from academy.apps.accounts.models import User
from academy.core.import_export.user import UserImportExport


class Command(BaseCommand):
    help = 'Export User to Json'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True)

    def handle(self, *args, **options):
        file_path = options['file']
        users = User.objects.filter(is_superuser=False, profile__isnull=False).all()
        import_export = UserImportExport(file_path=file_path)
        import_export.export_data(users)
        print(f'File Exported to {file_path}')

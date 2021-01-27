from django.core.management.base import BaseCommand

from academy.apps.accounts.models import User
from academy.core.import_export.user import UserExport


class Command(BaseCommand):
    help = 'Export User to Json'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True)
        parser.add_argument('--emails', nargs='+', type=str, required=False)

    def handle(self, *args, **options):
        file_path = options['file']
        user_emails = options.get('emails')

        if user_emails:
            users = User.objects.filter(email__in=user_emails)
        else:
            users = User.objects.filter(is_superuser=False, profile__isnull=False).all()

        if users:
            import_export = UserExport(file_path=file_path)
            import_export.export_data(users)
            print(f'File Exported to {file_path}')
        else:
            print('Data user is empty')

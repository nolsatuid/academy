from django.core.management.base import BaseCommand

from academy.core.import_export.user import UserImportExport


class Command(BaseCommand):
    help = 'Import User'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True)

    def handle(self, *args, **options):
        file_path = options['file']
        import_export = UserImportExport(file_path=file_path)
        import_export.import_data()
        print(f'Import Finished')

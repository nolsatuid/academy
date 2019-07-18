from django.core.management.base import BaseCommand

from academy.apps.accounts.models import User
from post_office.models import Email, STATUS


class Command(BaseCommand):
    help = 'Mark email user has_invalid_email to False'

    def handle(self, *args, **options):
        emails = Email.objects.filter(status=STATUS.failed)
        invalid_emails = []
        for email in emails:
            for log in email.logs.filter(status=STATUS.failed):
                if log.exception_type == 'SMTPRecipientsRefused':
                    invalid_emails = invalid_emails + email.to
                    break

        users = User.objects.filter(email__in=invalid_emails)
        users.update(has_valid_email=False)
        print(f'{len(invalid_emails)} users has invalid email')

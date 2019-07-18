from django.utils import timezone

from django.core.management.base import BaseCommand

from post_office.models import Email, STATUS


class Command(BaseCommand):
    help = 'Change status email failed to queued to resend'

    def handle(self, *args, **options):
        emails = Email.objects.filter(status=STATUS.failed, created__lt=timezone.now())
        failed = emails.count()
        emails.update(status=STATUS.queued)
        print('%s email success change status to queued' % failed)

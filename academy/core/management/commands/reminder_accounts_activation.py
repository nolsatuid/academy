from datetime import timedelta

from django.utils import timezone
from django.core.management.base import BaseCommand

from academy.apps.accounts.models import User


class Command(BaseCommand):
    help = 'Reminder acivation accounts'

    def handle(self, *args, **options):
        now = timezone.now()
        users = User.objects.filter(is_active=False)

        emails = []
        for user in users:
            delta = now.date() - user.date_joined.date()
            #reminder 1 day, 3 days, 7 days and multiplier 7
            if delta.days == 1 or delta.days == 3 or delta.days >= 7 and delta.days % 7 == 0:
                user.notification_register()
                emails.append(user.email)

        print(f"{len(emails)} emails, send reminder")

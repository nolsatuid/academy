from django.db import models
from django.conf import settings
from django.template.loader import render_to_string

from academy.apps.accounts.models import Inbox

from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from post_office import mail
from post_office.models import PRIORITY
from django_rq import job


class Broadcast(models.Model):
    title = models.CharField(max_length=220)
    VIA = (
        ('email', 'Email'),
        ('push_notification', 'Push Notification'),
        ('sms', 'SMS'),
    )
    via = MultiSelectField(choices=VIA)
    short_content = models.TextField(
        max_length=140, blank=True, null=True,
        help_text="Kontek untuk siaran via Push Notification dan SMS"
    )
    html_content = RichTextField(
        blank=True, null=True, help_text="Kontek untuk siaran via Email")

    def __str__(self):
        return self.title

    def preview(self, user):
        data = {
            'host': settings.HOST,
            'user': user,
            'body': self.html_content,
            'email_title': self.title
        }
        html_message = render_to_string(
            'emails/universal_template.html', context=data)
        return html_message

    @job
    def send(self, users):
        if 'email' in self.via:
            self.send_email(users)

    def send_email(self, users):
        kwargs_list = []
        for user in users:
            html_message = self.preview(user)
            Inbox.objects.create(
                user=user, subject=self.title, content=html_message)

            kwargs = {
                'recipients': [user.email],
                'sender': settings.DEFAULT_FROM_EMAIL,
                'subject': self.title,
                'html_message': html_message
            }
            kwargs_list.append(kwargs)
        mail.send_many(kwargs_list)

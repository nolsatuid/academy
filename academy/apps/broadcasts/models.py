import django_rq

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string

from academy.apps.accounts.models import Inbox, User

from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField


def _send(inbox_id, send_email, send_push_notif):
    inbox = Inbox.objects.get(id=inbox_id)
    inbox.send_notification(
        subject_as_content=True,
        send_email=send_email,
        send_push_notif=send_push_notif
    )


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
        # get setting appearance
        from academy.apps.offices import utils
        sett = utils.get_settings(serializer=True)

        data = {
            'host': settings.HOST,
            'user': user,
            'body': self.html_content,
            'email_title': self.title
        }
        data.update(sett)

        html_message = render_to_string(
            'emails/universal_template.html', context=data)
        return html_message

    def via_email(self):
        if 'email' in self.via:
            return True
        else:
            return False

    def via_push_notif(self):
        if 'push_notification' in self.via:
            return True
        else:
            return False

    def send(self, users):
        inbox_ids = []
        for user in users:
            html_message = self.preview(user)
            inbox = Inbox.objects.create(
                user=user, subject=self.title, content=html_message)
            inbox_ids.append(inbox.id)

        queue = django_rq.get_queue('high')
        for inbox_id in inbox_ids:
            kwargs = {
                'inbox_id': inbox_id,
                'send_email': self.via_email,
                'send_push_notif': self.via_push_notif
            }
            queue.enqueue(_send, **kwargs)

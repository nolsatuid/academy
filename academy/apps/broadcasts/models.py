from django.db import models

from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField


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

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
    content = RichTextField()

    def __str__(self):
        return self.title

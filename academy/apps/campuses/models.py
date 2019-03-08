from django.contrib.postgres.fields import ArrayField
from django.db import models

from academy.core.validators import validate_mobile_phone
from academy.core.utils import image_upload_path


class Campus(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=image_upload_path('campuses', use_dir_date=False), blank=True, null=True)
    description = models.TextField(blank=True, null=True, default=None)
    address = models.TextField(blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True, default=None,
                             validators=[validate_mobile_phone])
    open_registration = models.BooleanField(default=False)

    def __str__(self):
        return self.name

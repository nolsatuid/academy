from django.db import models

from academy.core.utils import image_upload_path


class LogoPartner(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=image_upload_path('partners', use_dir_date=False))
    display_order = models.PositiveSmallIntegerField()
    is_visible = models.BooleanField(default=True)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class LogoSponsor(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=image_upload_path('partners', use_dir_date=False))
    display_order = models.PositiveSmallIntegerField()
    is_visible = models.BooleanField(default=True)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.name

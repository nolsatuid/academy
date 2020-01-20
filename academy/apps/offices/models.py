from django.db import models

from academy.core.utils import image_upload_path
from ckeditor.fields import RichTextField


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
    image = models.ImageField(upload_to=image_upload_path('sponsors', use_dir_date=False))
    display_order = models.PositiveSmallIntegerField()
    is_visible = models.BooleanField(default=True)
    website = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class BannerInfo(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextField(help_text="Tuliskan informasi yang akan ditampilkan.")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

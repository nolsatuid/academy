from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.conf import settings

from academy.apps.accounts.models import User

from academy.core.utils import image_upload_path, generate_unique_slug
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from model_utils import Choices
from taggit.managers import TaggableManager
from meta.models import ModelMeta


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
    COLOR_STYLE = Choices(
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('primary', 'Primary'),
        ('info', 'Info')
    )
    color_style = models.CharField(
        max_length=50, choices=COLOR_STYLE,
        default=COLOR_STYLE.success
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def is_show(self):
        if not self.is_active:
            return False

        now = timezone.now().date()
        if not self.start_date and not self.end_date:
            return True
        elif self.start_date and not self.end_date:
            if self.start_date > now:
                return False
            elif self.start_date <= now:
                return True
        elif not self.start_date and self.end_date:
            if self.end_date >= now:
                return True
            elif self.end_date < now:
                return False
        elif self.start_date and self.end_date:
            if self.end_date >= now and self.end_date >= now:
                return True
            else:
                return False
        else:
            return False


class Page(ModelMeta, models.Model):
    title = models.CharField(_("Judul"), max_length=220)
    slug = models.SlugField(max_length=200, blank=True, help_text=_("Generate otomatis jika dikosongkan"))
    short_content = RichTextField(_("Konten Singkat"), config_name='basic_ckeditor')
    content = RichTextUploadingField(_("Konten"))
    image = models.FileField(_("Gambar"), upload_to="images/", blank=True)
    category = TaggableManager(_("Kategori"), help_text=_("Kategori dipisahkan dengan koma"))
    is_visible = models.BooleanField(_("Terlihat"), default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")
    STATUS = Choices(
        (1, 'draft', _("Konsep")),
        (2, 'publish', _("Terbit")),
    )
    status = models.PositiveIntegerField(choices=STATUS, default=STATUS.publish)

    _metadata = {
        'title': 'title',
        'description': 'content',
        'keywords': 'slug',
        'image': 'get_meta_image',
        'use_og': True
    }
    
    def get_meta_image(self):
        if self.image:
            return settings.HOST + '/static/website/' + self.image.url

    def __str__(self):
        return self.title 

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Page, self.title)
        else:  # create
            self.slug = generate_unique_slug(Page, self.title)
        super().save(*args, **kwargs)


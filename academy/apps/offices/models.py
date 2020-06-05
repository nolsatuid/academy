from rest_framework import serializers

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.conf import settings
from django.templatetags.static import static
from django.core.cache import cache

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
        'description': 'short_content',
        'keywords': 'get_category_list',
        'image': 'get_meta_image',
        'use_og': True
    }

    def get_meta_image(self):
        if self.image:
            return settings.HOST + '/static/website/' + self.image.url

    def get_category_list(self):
        return self.category.all().values_list('name', flat=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Page, self.title)
        else:  # create
            self.slug = generate_unique_slug(Page, self.title)
        super().save(*args, **kwargs)


class Setting(models.Model):
    name = models.CharField(max_length=50, default="Apperance")
    logo_light = models.ImageField(
        upload_to=image_upload_path('settings', use_dir_date=False),
        help_text=_("Akan digunakan pada latar terang"),
        blank=True, null=True
    )
    logo_dark = models.ImageField(
        upload_to=image_upload_path('settings', use_dir_date=False),
        help_text=_("Akan digunakan pada latar gelap"),
        blank=True, null=True
    )
    favicon = models.ImageField(
        upload_to=image_upload_path('settings', use_dir_date=False),
        blank=True, null=True
    )
    hide_logo = models.BooleanField(default=False)
    site_name = models.CharField(
        max_length=50, help_text=_("Menyumbunyikan logo pada Nav bar"))
    hide_site_name = models.BooleanField(
        default=False, help_text=_("Menyumbunyikan site name pada Nav bar"))
    footer_title = models.CharField(max_length=100, blank=True, null=True)
    footer_url = models.CharField(max_length=200, blank=True, null=True)
    COLOR_THEME = Choices(
        (1, 'danger', 'danger'),
        (2, 'warning', 'warning'),
        (3, 'primary', 'primary'),
        (4, 'success', 'success'),
        (5, 'dark', 'dark'),
    )
    color_theme = models.PositiveIntegerField(choices=COLOR_THEME, default=COLOR_THEME.danger)
    SIDEBAR_COLOR = Choices(
        (1, 'light', 'light'),
        (2, 'dark', 'dark'),
    )
    sidebar_color = models.PositiveIntegerField(choices=SIDEBAR_COLOR, default=SIDEBAR_COLOR.light)

    def __str__(self):
        return self.name

    def get_logo_light(self, with_host=False):
        if self.hide_logo:
            return ""

        if self.logo_light:
            logo = self.logo_light.url
        else:
            return static('website/images/logo/logo-polos-warna-30.png')

        if with_host:
            return settings.MEDIA_HOST + logo
        return logo

    def get_logo_dark(self, with_host=False):
        if self.hide_logo:
            return ""

        if self.logo_dark:
            logo = self.logo_dark.url
        else:
            return static('website/images/logo/logo-polos.png')

        if with_host:
            return settings.MEDIA_HOST + logo
        return logo

    def get_logo(self, with_host=False):
        if self.hide_logo:
            return ""

        if self.sidebar_color == self.SIDEBAR_COLOR.light:
            return self.get_logo_light(with_host)
        else:
            return self.get_logo_dark(with_host)

    def get_favicon(self):
        if self.favicon:
            return self.favicon.url
        else:
            return static('website/images/nolsatu.ico')

    @classmethod
    def get_data(cls):
        setting = cls.objects.first()
        key = f'setting-{settings.SESSION_COOKIE_DOMAIN}'
        expired = 3600 * 24 * 7

        # cache data to consume course app
        setting.set_cache_for_course(expired)

        query_cached = cache.get(key, None)
        if query_cached:
            return query_cached
        cache.set(key, setting, expired)
        return setting

    def set_cache_for_course(self, expired):
        key = f"course-appearance-{settings.SESSION_COOKIE_DOMAIN}"
        cached = cache.get(key, None)
        if not cached:
            cache.set(key, SettingSerializer(self).data, expired)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'setting-{settings.SESSION_COOKIE_DOMAIN}')
        cache.delete(f"course-appearance-{settings.SESSION_COOKIE_DOMAIN}")


class SettingSerializer(serializers.ModelSerializer):
    logo_light = serializers.CharField(source='get_logo_light')
    logo_dark = serializers.CharField(source='get_logo_dark')
    logo = serializers.CharField(source='get_logo')
    color_theme = serializers.CharField(source='get_color_theme_display')
    sidebar_color = serializers.CharField(source='get_sidebar_color_display')
    favicon = serializers.CharField(source='get_favicon')

    class Meta:
        model = Setting
        fields = ('__all__')


class ConfigEmail(models.Model):
    from_email = models.EmailField(max_length=255, verbose_name="Default From Email")
    email_host = models.CharField(max_length=255, verbose_name="Email Host")
    email_user = models.CharField(max_length=255, verbose_name="Email Host User")
    email_password = models.CharField(max_length=255, verbose_name="Email Host Password")
    email_port = models.IntegerField(verbose_name="Email Port")
    use_tls = models.BooleanField(verbose_name="Email Use TLS")
    recipient_email = models.EmailField(max_length=255, verbose_name="Default Recipient Email")


class AuthSetting(models.Model):
    name = models.CharField(max_length=50, default="Authorization")
    sign_with_btech = models.BooleanField(default=True, verbose_name="Signin with Btech Account")

    def __str__(self):
        return self.sign_with_btech
import django_rq
import pdfkit

from PIL import Image, ImageOps
from django.conf import settings
from django.db import models
from django.db.models import When, Case, Count, IntegerField, Q
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.tokens import default_token_generator
from django.templatetags.static import static
from django.utils.http import int_to_base36
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.cache import cache
from django.template.loader import get_template
from django.template.defaultfilters import slugify
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile

from academy.core.utils import image_upload_path, file_upload_path
from academy.core.validators import validate_mobile_phone
from academy.apps.students.models import TrainingStatus
from academy.apps.logs.models import LogTrainingStatus

from fcm_django.models import FCMDevice
from model_utils import Choices
from post_office import mail
from post_office.models import PRIORITY


class CustomUserManager(UserManager):
    def create_user(self, username, email, password, is_active=False, **extra_fields):
        user = super().create_user(username, email, password, is_active=False, **extra_fields)
        return user

    def registered(self):
        registered = self.exclude(Q(is_superuser=True) | Q(is_staff=True))
        return registered

    def actived(self):
        actived = self.registered().filter(is_active=True)
        return actived


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True, default=None,
                             validators=[validate_mobile_phone])
    ROLE = Choices(
        (1, 'student', 'Student'),
        (2, 'trainer', 'Trainer'),
        (2, 'company', 'Company'),
    )
    role = models.PositiveIntegerField(choices=ROLE, blank=True, null=True)
    VIA = Choices(
        (1, 'web', 'Web'),
        (2, 'mobile', 'Mobile'),
    )
    registered_via = models.PositiveIntegerField(choices=VIA, default=VIA.web, blank=True, null=True)
    has_valid_email = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def get_return_value(self):
        if self.email:
            return self.email
        elif self.username:
            return self.username
        elif self.name:
            return self.name

    def __str__(self):
        return self.get_return_value()

    @property
    def name(self):
        name = self.get_full_name()
        if not name:
            name = self.username
        return name

    def get_student(self):
        query_cached = cache.get(f'student-{self.id}', None)
        if query_cached:
            return query_cached
        query_cached = self.students.select_related('training').last()
        cache.set(f'student-{self.id}', query_cached, 3600)
        return query_cached

    def notification_register(self):
        data = {
            'token': default_token_generator.make_token(self),
            'uid': int_to_base36(self.id),
            'host': settings.HOST,
            'user': self,
            'email_title': 'Aktivasi Akun'
        }
        kwargs = {
            'recipients': [self.email],
            'sender': settings.DEFAULT_FROM_EMAIL,
            'subject': 'Aktivasi Akun',
            'priority': PRIORITY.now,
            'html_message': render_to_string('emails/register.html', context=data)
        }
        django_rq.enqueue(mail.send, **kwargs)

    def notification_status_training(self, training_materials):
        data = {
            'host': settings.HOST,
            'user': self,
            'training_materials': training_materials,
            'email_title': 'Status Pelatihan'
        }
        subject = 'Status Pelatihan'
        html_message = render_to_string('emails/training-status.html', context=data)
        inbox = Inbox.objects.create(user=self, subject=subject, content=html_message)
        inbox.send_notification(subject_as_content=True, send_email=False)

        kwargs = {
            'recipients': [self.email],
            'sender': settings.DEFAULT_FROM_EMAIL,
            'subject': subject,
            'html_message': html_message
        }
        django_rq.enqueue(mail.send, **kwargs)

    def get_count_training_status(self):
        student = self.get_student()
        materi_ids = student.training.materials.values_list('id', flat=True)
        count_status = self.training_status.filter(training_material_id__in=materi_ids).aggregate(
            graduate=Count(
                Case(When(status=TrainingStatus.STATUS.graduate, then=1),
                     output_field=IntegerField())
            ),
            not_yet=Count(
                Case(When(status=TrainingStatus.STATUS.not_yet, then=1),
                     output_field=IntegerField())
            ),
            repeat=Count(
                Case(When(status=TrainingStatus.STATUS.repeat, then=1),
                     output_field=IntegerField())
            )
        )
        return count_status

    def indicator_reached(self, status):
        if status['graduate'] >= settings.INDICATOR_GRADUATED and status['not_yet'] == 0:
            return True
        return False

    def save_training_status_to_log(self):
        LogTrainingStatus.objects.bulk_create([
            LogTrainingStatus(
                code=training.training_material.code,
                title=training.training_material.title,
                status=training.status,
                user=self,
                student=self.get_student()
            ) for training in self.training_status.exclude(Q(status=TrainingStatus.STATUS.not_yet) | Q(training_material=None))\
                    .select_related('training_material')
        ])

    def delete_training_status(self):
        self.training_status.all().delete()

    def get_training_materials(self):
        training_materials = []
        for ts in self.training_status.all():
            if ts.training_material:
                training_materials.append(ts.training_material)

        return training_materials

    def generate_auth_url(self):
        url = reverse('website:accounts:auth_user', args=[int_to_base36(self.id), default_token_generator.make_token(self)])
        return f'{settings.HOST}{url}'


class Profile(models.Model):
    user = models.OneToOneField('accounts.User', related_name='profile',
                                on_delete=models.CASCADE)
    address = models.TextField()
    GENDER = Choices(
        (1, 'male', 'Male'),
        (2, 'female', 'Female'),
    )
    gender = models.PositiveIntegerField(choices=GENDER, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to=image_upload_path('avatar'), blank=True, null=True)

    # Social fields
    linkedin = models.URLField(blank=True, max_length=255)
    git_repo = models.URLField(blank=True, max_length=255)
    blog = models.URLField(blank=True, max_length=255)
    facebook = models.URLField(blank=True, max_length=255)
    youtube = models.URLField(blank=True, max_length=255)
    twitter = models.CharField(blank=True, max_length=30)
    instagram = models.CharField(blank=True, max_length=30)
    telegram_id = models.CharField(blank=True, max_length=50)

    curriculum_vitae = models.FileField(upload_to=file_upload_path('cv'), blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            # Fit avatar to 200px x 200px
            img = Image.open(self.avatar)
            img = ImageOps.fit(img, (200, 200))
            img.save(self.avatar.path)

    def get_avatar(self, with_host=False):
        if self.avatar:
            avatar = self.avatar.url
        else:
            avatar = static('website/images/avatar_placeholder.png')

        if with_host:
            return settings.MEDIA_HOST + avatar
        return avatar


class Instructor(models.Model):
    user = models.OneToOneField('accounts.User', related_name='instructor',
                                on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # increment order manually because django din't let us have multiple auto field
        if not self.order:
            last_order = Instructor.objects.order_by('-order').first()
            self.order = 1
            if last_order is not None:
                self.order = last_order.order + 1

        super().save(*args, **kwargs)


class Inbox(models.Model):
    user = models.ForeignKey('accounts.User', related_name='recipient',
                             on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_html_content = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

    def preview(self):
        data = {
            'host': settings.HOST,
            'user': self.user,
            'body': self.content,
            'email_title': self.subject
        }
        html_message = render_to_string(
            'emails/universal_template.html', context=data)
        return html_message

    def send_notification(self, subject_as_content=False, send_email=True):
        title = "Info NolSatu" if subject_as_content else self.subject
        short_content = self.subject if subject_as_content else self.content

        # push notification
        devices_other = FCMDevice.objects.filter(user=self.user) \
            .exclude(type="ios")
        devices_other.send_message(data={
            "type": "notification",
            "title": title,
            "short_content": short_content,
            "inbox_id": self.id
        })

        devices_ios = FCMDevice.objects.filter(user=self.user, type="ios")
        devices_ios.send_message(
            title=title, body=short_content,
            sound=1, badge=1,
            data={
                "title": title,
                "short_content": short_content,
                "inbox_id": self.id
            }
        )

        # send email
        if send_email:
            html_message = self.preview()
            kwargs = {
                'recipients': [self.user.email],
                'sender': settings.DEFAULT_FROM_EMAIL,
                'subject': self.subject,
                'html_message': html_message
            }
            django_rq.enqueue(mail.send, **kwargs)


class Certificate(models.Model):
    """
    Model ini digunakan untuk menyimpan sertifikat secara jamak yang terkait dengan user.
    tidak terikat dengan model Graduate
    """
    title = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    user = models.ForeignKey('accounts.User', related_name='certificates',
                             on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to=image_upload_path('certificates'),
                                        blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number} - {self.title}"

    def generate(self):
        filename = 'certificate-%s.pdf' % slugify(self.user.name)
        filepath = '/tmp/%s' % filename
        html_template = get_template('backoffice/graduates/certificate-dev.html')

        last_name = (
            self.user.last_name if self.user.last_name
            else self.user.first_name
        )

        context = {
            'certificate': self,
            'user': self.user,
            'host': settings.HOST,
            'data_qr': f"{self.number}:{last_name}"
        }
        rendered_html = html_template.render(context)

        options = {
            'page-size': 'A4',
            'orientation': 'Landscape',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'no-outline': None
        }
        pdf = pdfkit.from_string(rendered_html, filepath, options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        certificate_file = open(filepath, 'rb')
        upload_file = SimpleUploadedFile(filename, certificate_file.read())
        self.certificate_file = upload_file
        self.save()

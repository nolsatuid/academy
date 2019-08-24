from datetime import timedelta

import pdfkit
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from model_utils.fields import AutoCreatedField

from academy.core.utils import image_upload_path


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Graduate(models.Model):
    certificate_number = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey('accounts.User', related_name='graduates',
                             on_delete=models.SET(get_sentinel_user))
    student = models.OneToOneField('students.Student', null=True, on_delete=models.SET_NULL)
    certificate_file = models.FileField(upload_to=image_upload_path('certificates'),
                                        blank=True, null=True)
    is_channeled = models.BooleanField(default=False)
    channeled_at = models.CharField(max_length=200, default='')
    created = AutoCreatedField()

    def __str__(self):
        return f"{self.user.name} - #{self.certificate_number}"

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()
        graduate = super().save(*args, **kwargs)
        return graduate

    def generate_certificate_number(self):
        batch = str(self.student.training.batch)
        batch = "0" + batch if len(batch) == 1 else batch

        user_id = str(self.user_id)
        user_id = "0" + user_id if len(user_id) == 1 else user_id

        date = self.created.strftime("%Y-%m%d")
        certificate_number = f"NS-{batch}{user_id}-{date}"
        return certificate_number

    def generate_certificate_file(self, force=False):
        if force:
            self.generate_and_save_certificate()

        if not self.certificate_file:
            self.generate_and_save_certificate()

    def generate_and_save_certificate(self):
        filename = 'certificate-%s.pdf' % slugify(self.user.name)
        filepath = '/tmp/%s' % filename
        html_template = get_template('backoffice/graduates/certificate.html')

        last_name = (
            self.user.last_name if self.user.last_name
            else self.user.first_name
        )

        context = {
            'graduate': self,
            'user': self.user,
            'host': settings.HOST,
            'data_qr': f"{self.certificate_number}:{last_name}"
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

    @property
    def valid_until(self):
        return self.created + timedelta(days=1095)

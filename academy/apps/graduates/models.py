from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class Graduate(models.Model):
    certificate_number = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey('accounts.User', related_name='graduates')
    student = models.OneToOneField('students.Student', null=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"{self.user.name} - #{self.certificate_number}"

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()
            self.save()

    def generate_certificate_number(self):
        batch = str(self.student.training.batch)
        batch = "0" + batch if len(batch) == 1 else batch

        user_id = str(self.user_id)
        user_id = "0" + user_id if len(user_id) == 1 else batch

        date = self.created.strftime("YYYY-MMDD")
        certificate_number = f"NS-{batch}{user_id}-{date}"
        return certificate_number

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class Graduate(models.Model):
    certificate_number = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey('accounts.User', related_name='graduates')
    student = models.OneToOneField('students.Student', null=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"{self.user.name} - #{self.certificate_number}"


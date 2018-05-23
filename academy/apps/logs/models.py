from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class LogTrainingStatus(models.Model):
    code = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    STATUS = Choices (
        (1, 'not_yet', _('Not Yet')),
        (2, 'graduate', _('Graduate')),
        (3, 'repeat', _('Repeat')),
    )
    status = models.PositiveIntegerField(choices=STATUS, blank=True, null=True)
    student = models.ForeignKey('students.Student', related_name='log_training_status')
    user = models.ForeignKey('accounts.User', related_name='log_training_status')
    created = AutoCreatedField()

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


class Training(models.Model):
    batch = models.PositiveIntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"batch {self.batch}"


class Student(models.Model):
    user = models.ForeignKey('accounts.User', related_name='students')
    training = models.ForeignKey('students.Training', related_name='students')
    STATUS = Choices (
        (1, 'selection', _('Selection')),
        (2, 'participants', _('Participants')),
        (3, 'repeat', _('Repeat')),
        (4, 'graduate', _('Graduate'))
    )
    status = models.PositiveIntegerField(choices=STATUS, default=STATUS.selection)

    def __str__(self):
        return self.user.email

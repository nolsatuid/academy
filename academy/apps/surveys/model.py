from django.contrib.postgres.fields import ArrayField
from django.db import models
from model_utils import Choices


class Survey(models.Model):
    WORKING_STATUS_CHOICES = Choices(
        (1, 'employee', 'Karyawan'),
        (2, 'student', 'Mahasiswa'),
        (3, 'unemployed', 'Belum Bekerja'),
        (99, 'other', 'Lain-lain')
    )

    GRADUATE_CHANNELED_TIME_CHOICES = Choices(
        (1, 'soon', 'Segera'),
        (99, 'other', 'Lain-lain')
    )

    TRUE_FALSE_CHOICES = (
        (True, 'Ya'),
        (False, 'Tidak')
    )

    user = models.OneToOneField('accounts.User', related_name='survey')
    working_status = models.PositiveIntegerField(choices=WORKING_STATUS_CHOICES)
    working_status_other = models.CharField(blank=True, null=True, default=None, max_length=150)
    graduate_channeled = models.BooleanField()
    graduate_channeled_when = models.PositiveIntegerField(choices=GRADUATE_CHANNELED_TIME_CHOICES)
    graduate_channeled_when_other = models.CharField(blank=True, null=True, default=None, max_length=150)
    channeled_location = ArrayField(models.CharField(blank=True, null=True, default=None, max_length=255), default=list)
    channeled_location_other = ArrayField(models.CharField(blank=True, null=True, default=None, max_length=255),
                                          default=list)

    def __str__(self):
        return self.user.username

    def get_channeled_location(self):
        return ','.join(self.channeled_location + self.channeled_location_other)

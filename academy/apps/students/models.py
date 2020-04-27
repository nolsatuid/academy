import django_rq

from django.db import models
from django.core.cache import cache
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from model_utils import Choices
from post_office import mail

from academy.core.email_utils import construct_email_args


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Training(models.Model):
    batch = models.CharField(max_length=255, unique=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    materials = models.ManyToManyField('TrainingMaterial', blank=True,
                                       related_name='trainings')
    link_group = models.URLField(blank=True, max_length=255)

    def __str__(self):
        return f"Batch {self.batch}"

    @classmethod
    def get_or_create_initial(cls):
        training = cls.objects.filter(is_active=True) \
            .exclude(batch__contains='NSC').order_by('batch').last()
        if not training:
            training = cls.objects.create(batch="0")
        return training


class StudentManager(models.Manager):
    def participants(self):
        return self.exclude(
            Q(user__is_superuser=True) | Q(status=Student.STATUS.selection)
        )

    def graduated(self):
        graduated = self.exclude(user__is_superuser=True) \
            .filter(status=Student.STATUS.graduate)
        return graduated

    def pre_test(self):
        return self.exclude(user__is_superuser=True) \
            .filter(status=Student.STATUS.pre_test)


class Student(models.Model):
    user = models.ForeignKey('accounts.User', related_name='students',
                             on_delete=models.SET(get_sentinel_user))
    training = models.ForeignKey('students.Training', related_name='students',
                                 null=True, on_delete=models.SET_NULL)
    STATUS = Choices(
        (1, 'selection', _('Selection')),
        (5, 'pre_test', _('Pre-Test')),
        (2, 'participants', _('Participants')),
        (3, 'repeat', _('Repeat')),
        (4, 'graduate', _('Graduate'))
    )
    status = models.PositiveIntegerField(choices=STATUS, default=STATUS.selection)
    objects = StudentManager()
    campus = models.ForeignKey('campuses.Campus', related_name='students',
                               on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email

    def notification_status(self):
        from academy.apps.accounts.models import Inbox

        # get setting appearance
        from academy.apps.offices import utils
        sett = utils.get_settings(serializer=True)

        if self.status == self.STATUS.participants:
            template = 'emails/change_to_participant.html'
            title = 'Selamat, Anda menjadi peserta'
        elif self.status == self.STATUS.pre_test:
            template = 'emails/change_to_pre_test.html'
            title = 'Selamat, Anda Mengikuti Test'
        elif self.status == self.STATUS.graduate:
            template = 'emails/change_to_graduate.html'
            title = 'Selamat, Anda lulus'
        else:
            return

        status = self.user.get_count_training_status()
        data = {
            'host': settings.HOST,
            'user': self.user,
            'link_group': self.training.link_group,
            'email_title': title,
            'graduate': status['graduate'],
            'indicator': settings.INDICATOR_GRADUATED
        }
        data.update(sett)

        html_message = render_to_string(template, context=data)
        inbox = Inbox.objects.create(user=self.user, subject=title, content=html_message)
        inbox.send_notification(subject_as_content=True, send_email=False)

        kwargs = construct_email_args(
            recipients=[self.user.email],
            subject=title,
            content=html_message
        )
        django_rq.enqueue(mail.send, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'student-{self.user.id}')

    def get_training_materials(self):
        if hasattr(self, 'graduate'):
            training_materials = self.user.get_training_materials()
        else:
            training_materials = self.training.materials.prefetch_related('training_status')
        return training_materials


class TrainingMaterial(models.Model):
    code = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.code

    def get_training_status(self, user):
        return self.training_status.filter(user=user).first()


class TrainingStatus(models.Model):
    training_material = models.ForeignKey(
        'students.TrainingMaterial', related_name='training_status',
        null=True, on_delete=models.CASCADE
    )
    STATUS = Choices(
        (1, 'not_yet', _('Not Yet')),
        (2, 'graduate', _('Graduate')),
        (3, 'repeat', _('Repeat')),
    )
    status = models.PositiveIntegerField(choices=STATUS, blank=True, null=True)
    user = models.ForeignKey('accounts.User', related_name='training_status',
                             on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return self.get_status_display()

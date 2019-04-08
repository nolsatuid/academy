from django.template import Library
from django.utils.safestring import mark_safe
from academy.apps.students.models import TrainingStatus

register = Library()

@register.filter
def get_status(materi, user=None):
    if not materi:
        return None

    trainig_status = materi.get_training_status(user)
    if not trainig_status:
        return None

    return trainig_status.status


@register.filter(name='training_status_display')
def status_to_display(status, styling=False):
    if status == TrainingStatus.STATUS.not_yet:
        status_display = 'Belum'
        class_bagde = 'secondary'
    elif status == TrainingStatus.STATUS.graduate:
        status_display = 'Lulus'
        class_bagde = 'primary'
    elif status == TrainingStatus.STATUS.repeat:
        status_display = 'Ulang'
        class_bagde = 'warning'
    else:
        return '-'

    if styling:
        return mark_safe('<span class="badge badge-%s">%s</span>' %
                         (class_bagde, status_display))
    return status_display

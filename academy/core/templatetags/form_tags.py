from django.template import Library
from django.utils.safestring import mark_safe

from academy.apps.students.models import Student, TrainingStatus

register = Library()

@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='status_display')
def status_to_display(status, styling=False):
    if status == Student.STATUS.selection:
        status_display = 'seleksi'
        class_bagde = 'secondary'
    elif status == Student.STATUS.pre_test:
        status_display = 'pre-test'
        class_bagde = 'info'
    elif status == Student.STATUS.participants:
        status_display = 'peserta'
        class_bagde = 'primary'
    elif status == Student.STATUS.repeat:
        status_display = 'mengulang'
        class_bagde = 'warning'
    elif status == Student.STATUS.graduate:
        status_display = 'lulus'
        class_bagde = 'success'
    else:
        return '-'

    if styling:
        return mark_safe('<span class="badge badge-%s">%s</span>' %
                         (class_bagde, status_display))
    return status_display

@register.filter
def get_status_student(user):
    student = user.get_student()
    if not student:
        return None

    return student.status


@register.filter(name='status_material_to_display')
def status_material_to_display(status, styling=False):
    if status == TrainingStatus.STATUS.not_yet:
        status_display = 'belum'
        class_bagde = 'secondary'
    elif status == TrainingStatus.STATUS.repeat:
        status_display = 'ulang'
        class_bagde = 'warning'
    elif status == TrainingStatus.STATUS.graduate:
        status_display = 'lulus'
        class_bagde = 'success'
    else:
        return '-'

    if styling:
        return mark_safe('<span class="badge badge-%s">%s</span>' %
                         (class_bagde, status_display))
    return status_display
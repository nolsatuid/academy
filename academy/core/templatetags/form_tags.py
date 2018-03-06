from django.template import Library
from django.utils.safestring import mark_safe

from academy.apps.students.models import Student

register = Library()

@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='status_display')
def status_to_display(status, styling=False):
    if status == Student.STATUS.selection:
        status_display = 'seleksi'
        class_bagde = 'secondary'
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

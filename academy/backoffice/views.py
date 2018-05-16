from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Count, Q
from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training

@staff_member_required
def index(request):
    data_dashboard = {
        'pendaftar': User.objects.exclude(is_superuser=True).exclude(is_staff=True).count(),
        'peserta': Student.objects.filter(status = Student.STATUS.participants).count(),
        'lulus': Student.objects.filter(status = Student.STATUS.graduate).count()
    }

    angkatan = Training.objects.order_by('batch')
    context = {
        'title': 'Dasbor',
        'data': data_dashboard,
        'angkatan': angkatan,
        'jumlah_pendaftar': angkatan.annotate(num_students=Count('students')),
        'jumlah_peserta': angkatan.filter(students__status = Student.STATUS.participants) \
            .annotate(num_participants=Count('students')),
        'jumlah_lulus': angkatan.filter(students__status = Student.STATUS.graduate) \
            .annotate(num_graduate=Count('students'))
    }

    return render(request, 'backoffice/index.html', context=context)

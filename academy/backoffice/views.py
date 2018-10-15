from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Count, Q
from django.db import connection
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
    truncate_date = connection.ops.date_trunc_sql('month', 'date_joined')
    users = User.objects.exclude(is_superuser=True).exclude(is_staff=True).extra({'month':truncate_date})
    users_month = users.values('month').annotate(Count('id')).order_by('month')
    
    context = {
        'title': 'Dasbor',
        'data': data_dashboard,
        'angkatan': angkatan,
        'jumlah_pendaftar': users_month,
        'jumlah_lulus': angkatan.filter(students__status = Student.STATUS.graduate) \
            .annotate(num_graduate=Count('students')),
        'jumlah_ulang': angkatan.filter(students__status = Student.STATUS.repeat) \
            .annotate(num_repeat=Count('students'))
    }
    
    return render(request, 'backoffice/index.html', context=context)

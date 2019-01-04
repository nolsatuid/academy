from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.db import connection
from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training

@staff_member_required
def index(request):
    data_dashboard = {
        'pendaftar': User.objects.registered().count(),
        'pengguna': User.objects.actived().count(),
        'peserta': Student.objects.participants().count(),
        'lulus': Student.objects.graduated().count()
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
        'jumlah_lulus': angkatan.annotate(num_graduate=Coalesce(Count('students', filter=Q(students__status=Student.STATUS.graduate)),0) or 0),
        'jumlah_ulang': angkatan.annotate(num_repeat=Coalesce(Count('students', filter=Q(students__status=Student.STATUS.repeat)),0) or 0)
    }
    
    return render(request, 'backoffice/index.html', context=context)

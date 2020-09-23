from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.db import connection
from django.http import HttpResponse

from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training
from academy.apps.offices.models import Setting, AuthSetting
from .form import SettingForm, ImportUserForm, AuthSettingForm


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
    users = User.objects.exclude(is_superuser=True).exclude(
        is_staff=True).extra({'month': truncate_date})
    users_month = users.values('month').annotate(Count('id')).order_by('month')

    context = {
        'title': 'Dasbor',
        'menu_active': 'dashboard',
        'data': data_dashboard,
        'angkatan': angkatan,
        'jumlah_pendaftar': users_month,
        'jumlah_lulus': angkatan.annotate(num_graduate=Coalesce(Count('students', filter=Q(students__status=Student.STATUS.graduate)), 0) or 0),
        'jumlah_ulang': angkatan.annotate(num_repeat=Coalesce(Count('students', filter=Q(students__status=Student.STATUS.repeat)), 0) or 0)
    }

    return render(request, 'backoffice/index.html', context=context)


@staff_member_required
def setting_appearance(request):
    setting = get_object_or_404(Setting, id=1)
    form = SettingForm(request.POST or None,
                       request.FILES or None, instance=setting)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit tampilan')
        return redirect('backoffice:setting_appearance')

    context = {
        'title': 'Pengaturan Tampilan',
        'menu_active': 'setting',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def setting_authorization(request):
    setting = get_object_or_404(AuthSetting, name="Authorization")
    form = AuthSettingForm(request.POST or None, instance=setting)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit pengaturan otorisasi')
        return redirect('backoffice:setting_authorization')

    context = {
        'title': 'Pengaturan Otorisasi',
        'menu_active': 'setting',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def import_users(request):
    form = ImportUserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        csv_buffer = form.import_data()
        response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=reject-data.csv'
        return response

    context = {
        'title': 'Impor Pengguna',
        'menu_active': 'setting',
        'form': form,
        'custom_button_title': 'Impor Data'
    }
    return render(request, 'backoffice/form.html', context)

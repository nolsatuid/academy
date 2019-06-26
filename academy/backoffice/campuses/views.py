from django.http import HttpResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.core.utils import pagination
from academy.apps.campuses.models import Campus
from academy.apps.students.models import Student
from academy.apps.accounts.models import User
from academy.backoffice.campuses.forms import CampusForm, ParticipantsFilterForm, BaseFilterForm


@staff_member_required
def index(request):
    campus_list = Campus.objects.order_by('name')

    context = {
        'title': 'Kampus',
        'page_active': 'campus',
        'campuses': campus_list
    }
    return render(request, 'backoffice/campuses/index.html', context)


@staff_member_required
def add(request):
    form = CampusForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah kampus')
        return redirect('backoffice:campuses:index')

    context = {
        'title': 'Tambah Kampus',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit(request, id):
    campus = get_object_or_404(Campus, id=id)
    form = CampusForm(request.POST or None, request.FILES or None, instance=campus)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit kampus')
        return redirect('backoffice:campuses:index')

    context = {
        'title': 'Edit Kampus',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    campus = get_object_or_404(Campus, id=id)
    campus.delete()
    messages.success(request, 'Berhasil hapus kampus')
    return redirect('backoffice:campuses:index')


@staff_member_required
def details(request, id):
    campus = get_object_or_404(Campus, id=id)

    context = {
        'title': 'Edit Kampus',
        'campus': campus
    }
    return render(request, 'backoffice/campuses/details.html', context)


@staff_member_required
def participants(request):
    user_ids = Student.objects.filter(status=Student.STATUS.participants, campus__isnull=False) \
        .distinct('user_id').values_list('user_id', flat=True)
    user_list = User.objects.exclude(is_superuser=True).exclude(is_staff=True) \
        .filter(id__in=user_ids)
    user_count = user_list.count()

    download = request.GET.get('download', '')
    form = ParticipantsFilterForm(request.GET or None)
    if form.is_valid():
        user_list = form.get_data()
        if download:
            csv_buffer = form.generate_to_csv()
            response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=daftar-peserta.csv'
            return response

    page = request.GET.get('page', 1)
    users, page_range = pagination(user_list, page)

    context = {
        'title': 'Peserta',
        'page_active': 'participants',
        'users': users,
        'form': form,
        'user_count': user_count,
        'filter_count': user_list.count(),
        'query_params': 'name=%s&start_date=%s&end_date=%s&status=%s&batch=%s' % (request.GET.get('name', ''),
            request.GET.get('start_date', ''), request.GET.get('end_date', ''), request.GET.get('status', 2), request.GET.get('batch', '')),
        'page_range': page_range
    }
    return render(request, 'backoffice/campuses/participant.html', context)


@staff_member_required
def users_selection(request):
    user_ids = Student.objects.exclude(status=Student.STATUS.graduate).filter(campus__isnull=False) \
        .distinct('user_id').values_list('user_id', flat=True)
    user_list = User.objects.exclude(is_superuser=True).exclude(is_staff=True) \
        .filter(id__in=user_ids)
    user_count = user_list.count()

    download = request.GET.get('download', '')
    form = BaseFilterForm(request.GET or None)
    if form.is_valid():
        user_list = form.get_data()
        if download:
            csv_buffer = form.generate_to_csv()
            response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=daftar-pengguna-nolsatu-kampus.csv'
            return response

    page = request.GET.get('page', 1)
    users, page_range = pagination(user_list, page)

    context = {
        'title': 'Pengguna Nolsatu Kampus',
        'page_active': 'user',
        'users': users,
        'form': form,
        'user_count': user_count,
        'filter_count': user_list.count(),
        'query_params': 'name=%s&start_date=%s&end_date=%s&status=%s&batch=%s' % (request.GET.get('name', ''),
            request.GET.get('start_date', ''), request.GET.get('end_date', ''), request.GET.get('status', ''), request.GET.get('batch', '')),
        'page_range': page_range
    }
    return render(request, 'backoffice/campuses/participant.html', context)

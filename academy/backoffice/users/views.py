from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory

from academy.apps.accounts.models import User
from academy.apps.students.models import Student, TrainingMaterial

from .forms import (BaseFilterForm, ParticipantsFilterForm, ChangeStatusTraining,
                    BaseStatusTrainingFormSet)


@staff_member_required
def index(request):
    user_ids = Student.objects.distinct('user_id').values_list('user_id', flat=True)
    users = User.objects.exclude(is_superuser=True).exclude(is_staff=True) \
        .filter(id__in=user_ids)
    user_count = users.count()

    download = request.GET.get('download', '')
    form = BaseFilterForm(request.GET or None)
    if form.is_valid():
        users = form.get_data()
        if download:
            csv_buffer = form.generate_to_csv()
            response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=daftar-pengguna.csv'
            return response

    context = {
        'title': 'Pengguna',
        'page_active': 'user',
        'users': users,
        'form': form,
        'user_count': user_count,
        'filter_count': users.count()
    }
    return render(request, 'backoffice/users/index.html', context)


@staff_member_required
def details(request, id):
    user = get_object_or_404(User, id=id)

    context = {
        'user': user,
        'page_active': 'user',
        'title': 'User Detail',
        'student': user.get_student()
    }
    return render(request, 'backoffice/users/details.html', context)


@staff_member_required
def participants(request):
    user_ids = Student.objects.filter(status=Student.STATUS.participants) \
        .distinct('user_id').values_list('user_id', flat=True)
    users = User.objects.exclude(is_superuser=True).exclude(is_staff=True) \
        .filter(id__in=user_ids)
    user_count = users.count()

    download = request.GET.get('download', '')
    form = ParticipantsFilterForm(request.GET or None)
    if form.is_valid():
        users = form.get_data()
        if download:
            csv_buffer = form.generate_to_csv()
            response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=daftar-peserta.csv'
            return response

    context = {
        'title': 'Peserta',
        'page_active': 'participants',
        'users': users,
        'form': form,
        'user_count': user_count,
        'filter_count': users.count()
    }
    return render(request, 'backoffice/users/index.html', context)


@staff_member_required
def change_to_participant(request, id):
    user = get_object_or_404(User, id=id)
    student = user.get_student()

    if student.status == Student.STATUS.selection:
        student.status = Student.STATUS.participants
        student.save(update_fields=['status'])
        student.notification_status()

        messages.success(request, 'Status berhasil diubah menjadi peserta')
        return redirect('backoffice:users:details', id=user.id)

    messages.success(request, 'Maaf, pengguna ini sudah menjadi peserta atau sudah lulus')
    return redirect('backoffice:users:index')


@staff_member_required
def status_training(request, id):
    user = get_object_or_404(User, id=id)
    training_materials = TrainingMaterial.objects.prefetch_related('training_status')

    ChangeStatusFormSet = formset_factory(ChangeStatusTraining, formset=BaseStatusTrainingFormSet)

    initial = [
        {
            'training_material': materi.id,
            'status': materi.get_training_status(user).status \
                if materi.get_training_status(user) else 1
        }
        for materi in training_materials
    ]

    formset = ChangeStatusFormSet(data=request.POST or None, initial=initial,
                                  training_materials=training_materials)

    if formset.is_valid():
        formset.save(user)
        messages.success(request, f'Status Pelatihan {user.get_full_name()} berhasil disimpan')

    context = {
        'formset': formset,
        'title': 'Daftar Pelatihan',
        'training_materials': training_materials,
        'student': request.user.get_student(),
        'user': user
    }
    # return render(request, 'backoffice/users/status_training.html', context)
    return render(request, 'backoffice/form-change-status.html', context)

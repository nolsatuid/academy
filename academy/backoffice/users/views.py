from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training
from academy.core.utils import pagination
from .forms import (BaseFilterForm, ParticipantsFilterForm, ChangeStatusTraining,
                    BaseStatusTrainingFormSet, TrainingForm, StudentForm, ChangeStatusForm, ChangeToParticipantForm)


@staff_member_required
def index(request):
    user_ids = Student.objects.exclude(status=Student.STATUS.graduate).filter(campus__isnull=True) \
        .exclude(user__username='deleted').distinct('user_id').values_list('user_id', flat=True)
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
            response['Content-Disposition'] = 'attachment; filename=daftar-pengguna.csv'
            return response

    page = request.GET.get('page', 1)
    users, page_range = pagination(user_list, page)

    context = {
        'title': 'Pengguna',
        'page_active': 'user',
        'users': users,
        'form': form,
        'user_count': user_count,
        'filter_count': user_list.count(),
        'query_params': 'name=%s&start_date=%s&end_date=%s&status=%s&batch=%s' % (request.GET.get('name', ''),
            request.GET.get('start_date', ''), request.GET.get('end_date', ''), request.GET.get('status', ''), request.GET.get('batch', '')),
        'page_range': page_range
    }
    return render(request, 'backoffice/users/index.html', context)


@staff_member_required
def details(request, id):
    user = get_object_or_404(User, id=id)
    survey = None
    if hasattr(user, 'survey'):
        survey = user.survey

    context = {
        'user': user,
        'page_active': 'user',
        'title': 'User Detail',
        'survey': survey,
        'student': user.get_student(),
        'to_participant_form': ChangeToParticipantForm(initial={
            'training': user.get_student().training
        })
    }
    return render(request, 'backoffice/users/details.html', context)


@staff_member_required
def participants(request):
    user_ids = Student.objects.filter(status=Student.STATUS.participants) \
        .exclude(user__username='deleted').distinct('user_id').values_list('user_id', flat=True)
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
        'query_params':'name=%s&start_date=%s&end_date=%s&status=%s&batch=%s' % (request.GET.get('name', ''),
            request.GET.get('start_date', ''), request.GET.get('end_date', ''), request.GET.get('status', 2), request.GET.get('batch', '')),
        'page_range': page_range
    }
    return render(request, 'backoffice/users/index.html', context)


@staff_member_required
def change_to_participant(request, id):
    user = get_object_or_404(User, id=id)
    student = user.get_student()

    if student.status == Student.STATUS.selection:
        form = ChangeToParticipantForm(request.POST or None)

        if form.is_valid():
            form.save(student)

            messages.success(request, 'Status berhasil diubah menjadi peserta')
            return redirect('backoffice:users:details', id=user.id)

    messages.success(request, 'Maaf, pengguna ini sudah menjadi peserta atau sudah lulus')
    return redirect('backoffice:users:index')


@staff_member_required
def status_training(request, id):
    user = get_object_or_404(User, id=id)
    student = user.get_student()
    training_materials = student.training.materials.prefetch_related('training_status')

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
        user.notification_status_training(training_materials)
        messages.success(request, f'Status Pelatihan {user.get_full_name()} berhasil disimpan')

    context = {
        'formset': formset,
        'title': 'Daftar Pelatihan',
        'training_materials': training_materials,
        'student': request.user.get_student(),
        'user': user
    }
    return render(request, 'backoffice/form-change-status.html', context)


@staff_member_required
def batch_training(request):
    form = TrainingForm(request.POST or None)
    trainings = Training.objects.order_by('batch')

    if form.is_valid():
        training = form.save()
        messages.success(request, f'Pelatihan Angkatan {training.batch} telah di tambahkan')

    context = {
        'form': form,
        'title': 'Tambah Angkatan',
        'trainings': trainings
    }

    return render(request, 'backoffice/form-batch-training.html', context)


@staff_member_required
def edit_batch_training(request, id):
    training = get_object_or_404(Training, id=id)
    form = TrainingForm(data=request.POST or None, instance=training)
    trainings = Training.objects.order_by('batch')

    if form.is_valid():
        training = form.save()
        messages.success(request, f'Pelatihan Angkatan {training.batch} telah di ubah')
        return redirect('backoffice:users:batch_training')

    context = {
        'form': form,
        'title': 'Edit Angkatan',
        'trainings': trainings
    }

    return render(request, 'backoffice/form-batch-training.html', context)


@staff_member_required
def edit_student_batch(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    form = StudentForm(data=request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, f'Berhasil ubah data angkatan {student.user.name}')
        return redirect('backoffice:users:details', id=student.user.id)

    context = {
        'form': form,
        'title': 'Ubah Data Angkatan',
        'title_extra': student.user.name,
    }

    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit_status(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    form = ChangeStatusForm(data=request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, f'Berhasil ubah status {student.user.name}')
        return redirect('backoffice:users:details', id=student.user.id)

    context = {
        'form': form,
        'title': 'Ubah status',
        'title_extra': student.user.name,
    }

    return render(request, 'backoffice/form.html', context)
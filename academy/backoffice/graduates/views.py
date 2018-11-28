import csv

from io import StringIO

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory

from academy.apps.graduates.models import Graduate
from academy.apps.students.models import Student, TrainingMaterial
from academy.apps.accounts.models import User
from academy.backoffice.users.forms import ChangeStatusTraining, BaseStatusTrainingFormSet
from .forms import ParticipantsRepeatForm


@staff_member_required
def index(request):
    graduates = Graduate.objects.select_related('user')
    download = request.GET.get('download', '')
    
    if download:
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'Nama', 'No.Sertifikat', 'Email', 'No. Ponsel'
        ])

        for index, graduate in enumerate(graduates, 1):
            writer.writerow([
                index, graduate.user.name, graduate.certificate_number,
                graduate.user.email, graduate.user.phone
            ])

        response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=daftar-lulusan.csv'
        return response

    paginator = Paginator(graduates, 25)
    page = request.GET.get('page', 1)
    try:
        data_graduates = paginator.page(page)
    except PageNotAnInteger:
        data_graduates = paginator.page(1)
    except EmptyPage:
        data_graduates = paginator.page(paginator.num_pages)

    max_index = len(paginator.page_range)
    index = data_graduates.number
    start_index = max_index - 5 if index > max_index - 3 else (index - 3 if index > 3 else 0)
    end_index = 5 if index <= 3 else (index + 2 if index < max_index - 2 else max_index)
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'graduates': graduates,
        'title': "Daftar Lulusan",
        'data_graduates': data_graduates,
        'page_range': page_range
    }
    return render(request, 'backoffice/graduates/index.html', context)


@staff_member_required
def candidates(request):
    training_count = TrainingMaterial.objects.all().count()
    user_ids = Student.objects.filter(status=Student.STATUS.participants) \
        .order_by('user_id').distinct('user_id').values_list('user_id', flat=True)

    users = User.objects.filter(id__in=user_ids)

    cantidate_graduates = []
    cantidate_repeats = []
    for user in users:
        status = user.get_count_training_status()
        if status['graduate'] >= settings.INDICATOR_GRADUATED:
            if user.indicator_reached(status):
                user.is_graduate = True
            else:
                user.is_graduate = False
            cantidate_graduates.append(user)
        elif status['repeat'] >= settings.INDICATOR_REPEATED:
            cantidate_repeats.append(user)

    download_graduates = request.GET.get('download-calon-lulusan', '')    
    if download_graduates:
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'Nama', 'Email', 'No. Ponsel'
        ])

        for index, candidate_graduate in enumerate(cantidate_graduates, 1):
            writer.writerow([
                index, candidate_graduate.name, candidate_graduate.email, candidate_graduate.phone
            ])

        response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=daftar-calon-lulusan.csv'
        return response

    download_repeats = request.GET.get('download-calon-mengulang', '')    
    if download_repeats:
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'Nama', 'Email', 'No. Ponsel'
        ])

        for index, candidate_repeats in enumerate(cantidate_repeats, 1):
            writer.writerow([
                index, candidate_repeats.name, candidate_repeats.email, candidate_repeats.phone
            ])

        response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=daftar-calon-mengulang.csv'
        return response

    paginator_graduates = Paginator(cantidate_graduates, 25)
    page_graduates = request.GET.get('page_graduates', 1)
    try:
        data_candidate_graduates = paginator_graduates.page(page_graduates)
    except PageNotAnInteger:
        data_candidate_graduates = paginator_graduates.page(1)
    except EmptyPage:
        data_candidate_graduates = paginator_graduates.page(paginator_graduates.num_pages)

    max_index_graduates = len(paginator_graduates.page_range)
    index_graduates = data_candidate_graduates.number
    start_index_graduates = max_index_graduates - 5 if index_graduates > max_index_graduates - 3 else (index_graduates - 3 if index_graduates > 3 else 0)
    end_index_graduates = 5 if index_graduates <= 3 else (index_graduates + 2 if index_graduates < max_index_graduates - 2 else max_index_graduates)
    page_range_graduates = list(paginator_graduates.page_range)[start_index_graduates:end_index_graduates]

    paginator_repeats = Paginator(cantidate_repeats, 25)
    page_repeats = request.GET.get('page_repeats', 1)
    try:
        data_candidate_repeats = paginator_repeats.page(page_repeats)
    except PageNotAnInteger:
        data_candidate_repeats = paginator_repeats.page(1)
    except EmptyPage:
        data_candidate_repeats = paginator_repeats.page(paginator_repeats.num_pages)

    max_index_repeats = len(paginator_repeats.page_range)
    index_repeats = data_candidate_repeats.number
    start_index_repeats = max_index_repeats - 5 if index_repeats > max_index_repeats - 3 else (index_repeats - 3 if index_repeats > 3 else 0)
    end_index_repeats = 5 if index_repeats <= 3 else (index_repeats + 2 if index_repeats < max_index_repeats - 2 else max_index_repeats)
    page_range_repeats = list(paginator_repeats.page_range)[start_index_repeats:end_index_repeats]


    context = {
        'title': 'Kandidat',
        'cantidate_graduates': cantidate_graduates,
        'cantidate_repeats': cantidate_repeats,
        'indicator': settings.INDICATOR_GRADUATED,
        'repeat_indicator': settings.INDICATOR_REPEATED,
        'training_count': training_count,
        'page_range_graduates': page_range_graduates,
        'page_range_repeats': page_range_repeats,
        'data_candidate_graduates': data_candidate_graduates,
        'data_candidate_repeats': data_candidate_repeats,        
    }
    return render(request, 'backoffice/graduates/candidates.html', context)


@staff_member_required
@transaction.atomic
def candidate_to_graduates(request, id):
    user = get_object_or_404(User, id=id)
    status = user.get_count_training_status()
    if user.indicator_reached(status):
        user.save_training_status_to_log()
        Graduate.objects.create(user=user, student=user.get_student())

        student = user.get_student()
        student.status = Student.STATUS.graduate
        student.save(update_fields=['status'])
        student.notification_status()
        # user.delete_training_status()

        messages.success(request, f'Berhasil proses {user.name} menjadi lulusan')
        return redirect('backoffice:graduates:index')

    messages.warning(request, f'{user.name} belum memenuhi indikator kelulusan')
    return redirect('backoffice:graduates:candidates')


@staff_member_required
def details(request, id):
    graduate = get_object_or_404(Graduate, id=id)
    survey = None
    if hasattr(graduate.user, 'survey'):
        survey = graduate.user.survey

    context = {
        'graduate': graduate,
        'user': graduate.user,
        'title': 'Profil Lulusan',
        'student': graduate.student,
        'survey': survey
    }
    return render(request, 'backoffice/graduates/details.html', context)


@staff_member_required
def participants_repeat(request):
    form = ParticipantsRepeatForm(request.POST or None)

    if form.is_valid():
        sent = form.send_notification()
        messages.warning(request, f'{sent} pemberitahuan berhasil dikirim')

    context = {
        'title': 'Peserta mengulang',
        'form': form
    }
    return render(request, 'backoffice/graduates/participants_repeat.html', context)


@staff_member_required
def status_training(request, id):
    graduate = get_object_or_404(Graduate, id=id)
    user = graduate.user
    student = graduate.student
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
        'student': student,
        'user': user
    }
    return render(request, 'backoffice/form-change-status.html', context)


@staff_member_required
def show_certificate(request, id):
    graduate = get_object_or_404(Graduate, id=id)
    user = graduate.user
    force = False

    if request.GET.get('regenerate') and request.GET['regenerate'] == 'yes':
        force = True

    graduate.generate_certificate_file(force)

    context = {
        'title': f'Certificate {graduate.certificate_number}',
        'graduate': graduate
    }
    return render(request, 'backoffice/graduates/show_certificate.html',
                  context)

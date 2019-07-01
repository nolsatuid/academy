import csv

from io import StringIO

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import formset_factory
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from academy.core.utils import pagination
from academy.apps.graduates.models import Graduate
from academy.apps.students.models import Student, TrainingMaterial, TrainingStatus
from academy.apps.accounts.models import User
from academy.backoffice.users.forms import ChangeStatusTraining
from .forms import (
    ParticipantsRepeatForm, AddTrainingStatus, GraduateTrainingStatusFormSet, BaseFilterForm,
    GraduateHasChanneledForm
)


class IndexView(View):
    form_class = BaseFilterForm
    template_name = 'backoffice/graduates/index.html'
    title = 'Data Lulusan'
    page_active = 'graduates'
    file_title = 'daftar-lulusan.csv'

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        graduates = Graduate.objects.select_related('user').order_by('id')
        graduates_count = graduates.count()
        download = request.GET.get('download', '')

        form = self.form_class(request.GET or None)
        if form.is_valid():
            graduates = form.get_data()
            if download:
                csv_buffer = form.generate_to_csv()
                response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
                response['Content-Disposition'] = f'attachment; filename={self.file_title}'
                return response

        page = request.GET.get('page', 1)
        data_graduates, page_range = pagination(graduates, page)

        context = {
            'graduates': graduates,
            'title': self.title,
            'page_active': self.page_active,
            'data_graduates': data_graduates,
            'page_range': page_range,
            'form': form,
            'channeled_form': GraduateHasChanneledForm(),
            'graduates_count': graduates_count,
            'filter_count': graduates.count(),
        }
        return render(request, self.template_name, context)


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

    page_graduates = request.GET.get('page_graduates', 1)
    data_candidate_graduates, page_range_graduates = pagination(cantidate_graduates, page_graduates)

    page_repeats = request.GET.get('page_repeats', 1)
    data_candidate_repeats, page_range_repeats = pagination(cantidate_repeats, page_repeats)

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
    # training materials get from user, not get from training/batch
    training_materials = user.get_training_materials()

    ChangeStatusFormSet = formset_factory(ChangeStatusTraining, formset=GraduateTrainingStatusFormSet)

    initial = [
        {
            'training_material': materi.id,
            'status': materi.get_training_status(user).status \
                if materi.get_training_status(user) else 1
        }
        for materi in training_materials
    ]

    formset = ChangeStatusFormSet(data=request.POST or None, initial=initial,
                                  graduate=graduate)

    if formset.is_valid():
        formset.save(user)
        user.notification_status_training(training_materials)
        messages.success(request, f'Status Pelatihan {user.get_full_name()} berhasil disimpan')

    context = {
        'formset': formset,
        'title': 'Daftar Pelatihan',
        'training_materials': training_materials,
        'student': student,
        'user': user,
        'graduate': graduate
    }
    return render(request, 'backoffice/form-change-status.html', context)


@staff_member_required
def show_certificate(request, id):
    graduate = get_object_or_404(Graduate, id=id)
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


@staff_member_required
def add_training_material(request, id):
    graduate = get_object_or_404(Graduate, id=id)
    user = graduate.user
    form = AddTrainingStatus(data=request.POST or None, user=user)

    if form.is_valid():
        form.save()
        messages.success(request, "Berhasil menambahkan materi")
        return redirect('backoffice:graduates:status_training', id)

    context = {
        'title': f'Tambah Materi ke {user.name}',
        'custom_button_title': 'Tambah',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete_training_status(request, id, graduate_id):
    training_status = get_object_or_404(TrainingStatus, id=id)
    training_status.delete()

    messages.success(request, 'Berhasil menghapus materi pelatihan')
    return redirect('backoffice:graduates:status_training', graduate_id)


@staff_member_required
def change_is_channeled(request):
    if request.POST:
        form = GraduateHasChanneledForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('backoffice:graduates:details', form.cleaned_data['graduate_id'])
        messages.success(request, 'Maaf, pengguna ini sudah menjadi peserta atau sudah lulus')
        return redirect('backoffice:graduates:index')

    id = request.GET['id']
    graduate = get_object_or_404(Graduate, id=id)
    graduate.is_channeled = False
    graduate.channeled_at = ''
    graduate.save()
    data = {
        'message': 'Berhasil Ubah Status'
    }
    return JsonResponse(data)

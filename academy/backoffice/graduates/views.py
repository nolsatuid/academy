from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
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

    context = {
        'graduates': graduates,
        'title': "Daftar Lulusan"
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

    context = {
        'title': 'Kandidat',
        'cantidate_graduates': cantidate_graduates,
        'cantidate_repeats': cantidate_repeats,
        'indicator': settings.INDICATOR_GRADUATED,
        'repeat_indicator': settings.INDICATOR_REPEATED,
        'training_count': training_count
    }
    return render(request, 'backoffice/graduates/candidates.html', context)


@staff_member_required
@transaction.atomic
def candidate_to_graduates(request, id):
    user = get_object_or_404(User, id=id)
    status = user.get_count_training_status()
    if user.indicator_reached(status):
        user.save_training_status_to_log()
        graduate = Graduate.objects.create(user=user, student=user.get_student())
        graduate.generate_certificate_number()

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

    context = {
        'graduate': graduate,
        'user': graduate.user,
        'title': 'Profil Lulusan',
        'student': graduate.student
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

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.db import transaction

from academy.apps.graduates.models import Graduate
from academy.apps.students.models import Student, TrainingMaterial
from academy.apps.accounts.models import User


def index(request):
    graduates = Graduate.objects.select_related('user')

    context = {
        'graduates': graduates,
        'title': "Daftar Lulusan"
    }
    return render(request, 'backoffice/graduates/index.html', context)


def candidates(request):
    training_count = TrainingMaterial.objects.all().count()
    user_ids = Student.objects.filter(status=Student.STATUS.participants) \
        .order_by('user_id').distinct('user_id').values_list('user_id', flat=True)

    users = User.objects.filter(id__in=user_ids)

    user_cantidates = []
    for user in users:
        status = user.get_count_training_status()
        if user.indicator_reached(status):
            user_cantidates.append(user)

    context = {
        'title': 'Calon Lulusan',
        'users': user_cantidates,
        'indicator': settings.INDICATOR_GRADUATED,
        'training_count': training_count
    }
    return render(request, 'backoffice/graduates/candidates.html', context)


@transaction.atomic
def candidate_to_graduates(request, id):
    user = get_object_or_404(User, id=id)
    status = user.get_count_training_status()
    if user.indicator_reached(status):
        user.save_training_status_to_log()
        Graduate.objects.create(user=user)

        student = user.get_student()
        student.status = Student.STATUS.graduate
        student.save(update_fields=['status'])
        # send email notification

        messages.success(request, f'Berhasil proses {user.name} menjadi lulusan')
        return redirect('backoffice:graduates:index')

    messages.warning(request, f'{user.name} belum memenuhi indikator kelulusan')
    return redirect('backoffice:graduates:candidates')

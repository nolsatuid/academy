from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.students.models import TrainingMaterial


def materials(request):
    user = request.user
    training_materials = TrainingMaterial.objects.prefetch_related('training_status')

    for materi in training_materials:
        print(materi.get_training_status(user))

    context = {
        'title': 'Daftar Pelatihan',
        'training_materials': training_materials,
        'student': request.user.get_student()
    }
    return render(request, 'dashboard/trainings/materials.html', context)

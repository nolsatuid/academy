from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.students.models import TrainingMaterial


@login_required
def materials(request):
    student = request.user.get_student()

    if student:
        training_materials = student.get_training_materials()
    else:
        training_materials = None

    context = {
        'title': 'Daftar Pelatihan',
        'menu_active': 'materi',
        'training_materials': training_materials,
        'student': student
    }
    return render(request, 'dashboard/trainings/materials.html', context)

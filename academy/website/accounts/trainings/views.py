from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.students.models import TrainingMaterial


def materials(request):
    training_materials = TrainingMaterial.objects.all()
    context = {
        'title': 'Daftar Pelatihan',
        'training_materials': training_materials,
        'student': request.user.get_student()
    }
    return render(request, 'dashboard/trainings/materials.html', context)

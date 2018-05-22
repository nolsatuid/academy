from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from academy.apps.students.models import TrainingMaterial
from .forms import TrainingMaterialForm


def index(request):
    training_materials = TrainingMaterial.objects.all()
    context = {
        'title': 'Materi Pelatihan',
        'training_materials': training_materials
    }
    return render(request, 'backoffice/training_materials/index.html', context)


def add(request):
    form = TrainingMaterialForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil menambah materi pelatihan')
        return redirect('backoffice:training_materials:index')

    context = {
        'title': 'Tambah Materi Pelatihan',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


def edit(request, id):
    training_material = get_object_or_404(TrainingMaterial, id=id)
    form = TrainingMaterialForm(data=request.POST or None, instance=training_material)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil mengubah materi pelatihan')
        return redirect('backoffice:training_materials:index')

    context = {
        'title': 'Edit Materi Pelatihan',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


def delete(request, id):
    TrainingMaterial.objects.get(id=id).delete()
    messages.success(request, 'Berhasil menghapus materi pelatihan')
    return redirect('backoffice:training_materials:index')

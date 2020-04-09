from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import formset_factory
from django.contrib.admin.views.decorators import staff_member_required

from academy.apps.students.models import TrainingMaterial, TrainingStatus
from .forms import (TrainingMaterialForm, StudentFilterForm, BaseStatusTrainingFormSet,
                    ChangeStatusTraining, BulkStatusTrainingForm)


@staff_member_required
def index(request):
    training_materials = TrainingMaterial.objects.all()
    context = {
        'title': 'Materi Pelatihan',
        'menu_active': 'materials',
        'training_materials': training_materials
    }
    return render(request, 'backoffice/training_materials/index.html', context)


@staff_member_required
def add(request):
    form = TrainingMaterialForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil menambah materi pelatihan')
        return redirect('backoffice:training_materials:index')

    context = {
        'title': 'Tambah Materi Pelatihan',
        'menu_active': 'materials',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit(request, id):
    training_material = get_object_or_404(TrainingMaterial, id=id)
    form = TrainingMaterialForm(data=request.POST or None, instance=training_material)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil mengubah materi pelatihan')
        return redirect('backoffice:training_materials:index')

    context = {
        'title': 'Edit Materi Pelatihan',
        'menu_active': 'materials',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    TrainingMaterial.objects.get(id=id).delete()
    messages.success(request, 'Berhasil menghapus materi pelatihan')
    return redirect('backoffice:training_materials:index')


@staff_member_required
def bulk_training_status(request):
    """
    bulk many to many change.
    """
    form = StudentFilterForm(request.GET or None)
    formset = None
    table_heading = {}

    if form.is_valid():
        students = form.get_data()
        cleaned_data = form.cleaned_data

        # set table heading
        table_heading['column_user'] = f"Angkatan {cleaned_data['batch'].batch}"
        table_heading['column_status'] = f"Status materi - {cleaned_data['training_materials'].title}"

        initial = []
        ChangeStatusFormSet = formset_factory(ChangeStatusTraining, formset=BaseStatusTrainingFormSet)
        for student in students:
            materi = student.training.materials.get(id=cleaned_data['training_materials'].id)
            initial.append({
                'user': student.user_id,
                'status': materi.get_training_status(student.user).status \
                    if materi.get_training_status(student.user) else 1
            })

        formset = ChangeStatusFormSet(data=request.POST or None, initial=initial,
                                      students=students)
        if formset.is_valid():
            formset.save(cleaned_data['training_materials'])
            messages.success(request, 'Berhasil edit status pelatihan')

    context = {
        'title': 'Status Pelatihan',
        'menu_active': 'materials',
        'form': form,
        'formset': formset,
        'table_heading': table_heading
    }
    return render(request, 'backoffice/training_materials/form-bulk-status.html', context)


@staff_member_required
def bulk_material_status(request):
    form = StudentFilterForm(request.GET or None)
    table_heading = {}
    student_ids = []
    bulk_form = None
    students = None
    if form.is_valid():
        cleaned_data = form.cleaned_data

        # set table heading
        table_heading['column_user'] = f"Angkatan {cleaned_data['batch'].batch}"
        table_heading['column_status'] = f"Status materi - {cleaned_data['training_materials'].title}"

        # form bulk
        student_ids = request.POST.getlist("students")
        bulk_form = BulkStatusTrainingForm(
            data=request.POST or None, student_ids=student_ids,
            training_material=cleaned_data['training_materials']
        )
        if bulk_form.is_valid():
            bulk_form.save()
            bulk_form.send_notification()
            messages.success(request, f"Berhasil ubah {len(student_ids)} data")

        # pass data students
        students = form.get_data()

    context = {
        'title': 'Status Pelatihan',
        'menu_active': 'user',
        'form': form,
        'students': students,
        'table_heading': table_heading,
        'bulk_form': bulk_form
    }
    return render(request, 'backoffice/training_materials/status-list.html', context)

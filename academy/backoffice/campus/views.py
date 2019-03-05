from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.campuses.model import Campus
from academy.backoffice.campus.form import CampusForm


@staff_member_required
def index(request):
    campus_list = Campus.objects.order_by('name')

    context = {
        'title': 'Kampus',
        'page_active': 'campus',
        'campus': campus_list
    }
    return render(request, 'backoffice/campus/index.html', context)


@staff_member_required
def add(request):
    form = CampusForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah kampus')
        return redirect('backoffice:campus:index')

    context = {
        'title': 'Tambah Kampus',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit(request, id):
    campus = get_object_or_404(Campus, id=id)
    form = CampusForm(request.POST or None, request.FILES or None, instance=campus)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit kampus')
        return redirect('backoffice:campus:index')

    context = {
        'title': 'Edit Kampus',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    campus = get_object_or_404(Campus, id=id)
    campus.delete()
    messages.success(request, 'Berhasil hapus kampus')
    return redirect('backoffice:campus:index')

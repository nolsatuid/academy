from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.backoffice.broadcasts.forms import BroadcastForm
from academy.apps.broadcasts.models import Broadcast


@staff_member_required
def index(request):
    broadcasts = Broadcast.objects.all()
    context = {
        'title': 'Broadcast Message',
        'menu_active': 'broadcast',
        'broadcasts': broadcasts
    }
    return render(request, 'backoffice/broadcasts/index.html', context)


@staff_member_required
def add(request):
    form = BroadcastForm(request.POST or None)

    if form.is_valid():
        broadcast = form.save()
        messages.success(request, f"Berhasil Menyiarkan {broadcast.title}")
        return redirect('backoffice:broadcasts:index')

    context = {
        'title': 'Add Broadcast Message',
        'menu_active': 'broadcast',
        'form': form
    }
    return render(request, 'backoffice/broadcasts/form-broadcasts.html', context)


@staff_member_required
def delete(request, id):
    broadcast = get_object_or_404(Broadcast, id=id)
    title = broadcast.title
    broadcast.delete()
    messages.success(request, f"Berhasil menghapus {title}")
    return redirect('backoffice:broadcasts:index')


@staff_member_required
def edit(request, id):
    broadcast = get_object_or_404(Broadcast, id=id)
    form = BroadcastForm(data=request.POST or None, instance=broadcast)

    if form.is_valid():
        broadcast = form.save()
        messages.success(request, f"Berhasil ubah data {broadcast.title}")
        return redirect('backoffice:broadcasts:index')

    context = {
        'title': 'Edit Broadcast Message',
        'menu_active': 'broadcast',
        'form': form
    }
    return render(request, 'backoffice/broadcasts/form-broadcasts.html', context)

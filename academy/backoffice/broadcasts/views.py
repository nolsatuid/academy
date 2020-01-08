from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.backoffice.broadcasts.forms import BroadcastForm
from academy.apps.broadcasts.models import Broadcast
from academy.apps.accounts.models import User


@staff_member_required
def index(request):
    broadcasts = Broadcast.objects.all()
    context = {
        'title': 'Pesan Siaran',
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
        'title': 'Tambah Pesan Siaran',
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
        'title': 'Edit Pesan Siaran',
        'menu_active': 'broadcast',
        'form': form
    }
    return render(request, 'backoffice/broadcasts/form-broadcasts.html', context)


@staff_member_required
def detail(request, id):
    broadcast = get_object_or_404(Broadcast, id=id)
    html_content = broadcast.preview(request.user) if 'email' in broadcast.via else None
    context = {
        'title': 'Detail Pesan Siaran',
        'menu_active': 'broadcast',
        'broadcast': broadcast,
        'html_content': html_content
    }
    return render(request, 'backoffice/broadcasts/detail.html', context)


@staff_member_required
def broadcast_now(request, id):
    broadcast = get_object_or_404(Broadcast, id=id)
    users = User.objects.registered().exclude(has_valid_email=False) \
        .exclude(email=None)
    broadcast.send(users)
    messages.success(request, f"Berhasil menyirkan pesan {broadcast.title}")
    return redirect("backoffice:broadcasts:index")

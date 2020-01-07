from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

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

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.offices.models import LogoSponsor
from academy.backoffice.sponsors.forms import SponsorForm


@staff_member_required
def index(request):
    sponsors = LogoSponsor.objects.order_by('display_order')

    context = {
        'title': 'Sponsor',
        'menu_active': 'sponsors',
        'sponsors': sponsors
    }
    return render(request, 'backoffice/sponsors/index.html', context)


@staff_member_required
def add(request):
    form = SponsorForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah sponsor')
        return redirect('backoffice:sponsors:index')

    context = {
        'title': 'Tambah Sponsor',
        'menu_active': 'sponsors',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit(request, id):
    sponsor = get_object_or_404(LogoSponsor, id=id)
    form = SponsorForm(request.POST or None, request.FILES or None, instance=sponsor)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit sponsor')
        return redirect('backoffice:sponsors:index')

    context = {
        'title': 'Edit Sponsor',
        'menu_active': 'sponsors',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    sponsor = get_object_or_404(LogoSponsor, id=id)
    sponsor.delete()
    messages.success(request, 'Berhasil hapus sponsor')
    return redirect('backoffice:sponsors:index')

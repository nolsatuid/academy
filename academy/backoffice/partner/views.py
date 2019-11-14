from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.offices.models import LogoPartner
from academy.backoffice.partner.form import PartnerForm


@staff_member_required
def index(request):
    partner_list = LogoPartner.objects.order_by('display_order')

    context = {
        'title': 'Mitra',
        'menu_active': 'partner',
        'partners': partner_list
    }
    return render(request, 'backoffice/partner/index.html', context)


@staff_member_required
def add(request):
    form = PartnerForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah mitra')
        return redirect('backoffice:partners:index')

    context = {
        'title': 'Tambah Mitra',
        'menu_active': 'partner',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def edit(request, id):
    partner = get_object_or_404(LogoPartner, id=id)
    form = PartnerForm(request.POST or None, request.FILES or None, instance=partner)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit mitra')
        return redirect('backoffice:partners:index')

    context = {
        'title': 'Edit Mitra',
        'menu_active': 'partner',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    partner = get_object_or_404(LogoPartner, id=id)
    partner.delete()
    messages.success(request, 'Berhasil hapus mitra')
    return redirect('backoffice:partners:index')

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.offices.models import ConfigEmail
from academy.backoffice.settings.form import ConfigEmailForm, TestEmailForm
from academy.apps.accounts.models import Certificate
from django.http import HttpResponse


@staff_member_required
def email_index(request):
    config_email = ConfigEmail.objects.filter(id=1).first()
    if not config_email:
        return redirect('backoffice:settings:email_edit')

    form = TestEmailForm(request.POST or None)
    if form.is_valid():
        form.send_email()
        messages.success(request, 'Email dikirim')
        return redirect('backoffice:settings:email_index')

    context = {
        'title': 'Pengaturan Email',
        'menu_active': 'setting',
        'form': form,
        'config': config_email
    }
    return render(request, 'backoffice/settings/email/index.html', context)


@staff_member_required
def email_edit(request):
    config_email = ConfigEmail.objects.filter(id=1).first()
    form = ConfigEmailForm(request.POST or None, instance=config_email)
    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil edit pengaturan email')
        return redirect('backoffice:settings:email_index')

    context = {
        'title': 'Edit Pengaturan Email',
        'menu_active': 'setting',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def certificate_preview(request):
    cert = Certificate.objects.first()
    return HttpResponse(cert.preview())

from django.shortcuts import render, redirect

from academy.apps.graduates.models import Graduate


def index(request):
    graduates = Graduate.objects.select_related('user')

    context = {
        'graduates': graduates,
        'title': "Daftar Lulusan"
    }
    return render(request, 'backoffice/graduates/index.html', context)

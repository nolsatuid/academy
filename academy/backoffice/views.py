from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def index(request):
    data_dashboard = {
        'pengguna': 10,
        'peserta': 20,
        'pendaftar': 30
    }

    context = {
        'title': 'Dasbor',
        'data': data_dashboard
    }

    return render(request, 'backoffice/index.html', context=context)

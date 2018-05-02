from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def index(request):
    context = {
        'title': 'Dasbor',
        'page_active': 'dasbor',
    }

    return render(request, 'backoffice/index.html', context=context)

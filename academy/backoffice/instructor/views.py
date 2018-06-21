from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from academy.apps.accounts.models import User
from academy.backoffice.instructor.forms import InstructorForm


@staff_member_required
def index(request):
    instructors = User.objects.filter(role=User.ROLE.trainer)
    context = {
        'title': 'Instruktur',
        'instructors': instructors
    }
    return render(request, 'backoffice/instructor/index.html', context)


@staff_member_required
def add(request):
    form = InstructorForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah instruktur')
        return redirect('backoffice:instructors:index')

    context = {
        'title': 'Tambah Instruktur',
        'form': form
    }
    return render(request, 'backoffice/instructor/add.html', context)


@staff_member_required
def ajax_find_user(request):
    q = request.GET.get('q')
    users = User.objects.filter(
        Q(first_name__contains=q) | Q(last_name__contains=q) | Q(email__contains=q) & Q(role=None)
    )

    data = {
        'users': [
            {
                'id': obj.id,
                'name': obj.name,
                'email': obj.email
            } for obj in users
        ]
    }

    return JsonResponse(data)

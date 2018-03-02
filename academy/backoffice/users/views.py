from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from academy.apps.accounts.models import User


@staff_member_required
def index(request):
    users = User.objects.exclude(is_superuser = True, is_staff = True)

    context = {
        'title': 'User',
        'page_active': 'user',
        'users': users
    }
    return render(request, 'backoffice/users/index.html', context)


@staff_member_required
def details(request, id):
    user = get_object_or_404(User, id=id)

    context = {
        'user': user,
        'page_active': 'user',
        'title': 'User Detail'
    }
    return render(request, 'backoffice/users/details.html', context)

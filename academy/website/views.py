from django.shortcuts import render

from academy.apps.accounts.models import User


def index(request):
    context = {
        'title': 'Home',
        'instructors': User.objects.filter(role=User.ROLE.trainer),
    }
    return render(request, 'website/home.html', context)


def faq(request):
    context = {
        'title': 'Tilil (Q&A)'
    }
    return render(request, 'website/faq.html', context)


def home(request):
    context = {
        'title': 'Home 2'
    }
    return render(request, 'website/home2.html', context)
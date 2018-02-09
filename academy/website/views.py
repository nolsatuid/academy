from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'website/home.html', context)


def home(request):
    context = {
        'title': 'Home 2'
    }
    return render(request, 'website/home2.html', context)
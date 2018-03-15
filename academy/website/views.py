from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'website/home.html', context)


def faq(request):
    context = {
        'title': 'Tilil'
    }
    return render(request, 'website/faq.html', context)


def home(request):
    context = {
        'title': 'Home 2'
    }
    return render(request, 'website/home2.html', context)


def error_404(request):
    return render(request, '404.html', {})


def error_500(request):
    return render(request, '500.html', {})
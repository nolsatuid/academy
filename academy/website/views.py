from django.shortcuts import render


def index(request):
    context = {
        'title': 'Alinguwa'
    }
    return render(request, 'website/index.html', context)
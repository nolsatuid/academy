from django.shortcuts import render, redirect
from django.conf import settings

from academy.apps.graduates.models import Graduate
from academy.apps.students.models import Student, TrainingMaterial
from academy.apps.accounts.models import User

def index(request):
    graduates = Graduate.objects.select_related('user')

    context = {
        'graduates': graduates,
        'title': "Daftar Lulusan"
    }
    return render(request, 'backoffice/graduates/index.html', context)


def candidates(request):
    training_count = TrainingMaterial.objects.all().count()
    user_ids = Student.objects.filter(status=Student.STATUS.participants) \
        .order_by('user_id').distinct('user_id').values_list('user_id', flat=True)
    
    users = User.objects.filter(id__in=user_ids)

    user_cantidates = []
    for user in users:
        status = user.get_count_training_status()
        
        if status['graduate'] >= settings.INDICATOR_GRADUATED and status['not_yet'] == 0:
            user_cantidates.append(user)
        
    context = {
        'title': 'Calon Lulusan',
        'users': user_cantidates,
        'indicator': settings.INDICATOR_GRADUATED,
        'training_count': training_count
    }
    return render(request, 'backoffice/graduates/candidates.html', context)

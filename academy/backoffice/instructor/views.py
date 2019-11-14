from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from academy.apps.accounts.models import User, Instructor
from academy.backoffice.instructor.forms import AddInstructorForm, EditInstructorForm


@staff_member_required
def index(request):
    instructors = Instructor.objects.order_by('order')
    context = {
        'title': 'Instruktur',
        'menu_active': 'instrukturs',
        'instructors': instructors
    }
    return render(request, 'backoffice/instructor/index.html', context)


@staff_member_required
def add(request):
    form = AddInstructorForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Berhasil tambah instruktur')
        return redirect('backoffice:instructors:index')

    context = {
        'title': 'Tambah Instruktur',
        'menu_active': 'instrukturs',
        'form': form
    }
    return render(request, 'backoffice/instructor/add.html', context)


@staff_member_required
def ajax_find_user(request):
    q = request.GET.get('q')
    users = User.objects.filter(
        Q(first_name__contains=q) | Q(last_name__contains=q) | Q(email__contains=q)
    ).exclude(role=User.ROLE.trainer)

    data = {
        'data': [
            {
                'id': user.id,
                'text': f'{user.name} ({user.email})',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'linked_in': user.profile.linkedin if hasattr(user, 'profile') else None,
                'specialization': user.profile.specialization if hasattr(user, 'profile') else None,
                'avatar': user.profile.avatar.url if hasattr(user, 'profile') and user.profile.avatar else None
            } for user in users
        ]
    }

    return JsonResponse(data)


@staff_member_required
def edit(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    form = EditInstructorForm(request.POST or None, request.FILES or None, initial={
        'user': f'{instructor.user.name} ({instructor.user.email})',
        'first_name': instructor.user.first_name,
        'last_name': instructor.user.last_name,
        'linked_in': instructor.user.profile.linkedin,
        'specialization': instructor.user.profile.specialization,
        'avatar': instructor.user.profile.avatar
    })

    if form.is_valid():
        form.save(instructor.user)
        messages.success(request, 'Berhasil edit instruktur')
        return redirect('backoffice:instructors:index')

    context = {
        'title': 'Edit Instruktur',
        'menu_active': 'instrukturs',
        'form': form
    }
    return render(request, 'backoffice/form.html', context)


@staff_member_required
def delete(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    instructor.user.role = None
    instructor.user.save()
    instructor.delete()
    messages.success(request, 'Berhasil hapus instruktur')
    return redirect('backoffice:instructors:index')

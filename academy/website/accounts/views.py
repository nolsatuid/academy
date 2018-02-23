from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404

from academy.apps.accounts.models import User
from academy.apps.students.models import Training
from . forms import CustomAuthenticationForm, SignupForm, ProfileForm, StudentForm


@login_required
def index(request):
    user = request.user

    if hasattr(user, 'profile'):
        context = {
            'title': 'Dashboard',
        }
        return render(request, 'dashboard/index.html', context)

    form = ProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(user)
        training = Training.objects.filter(is_active=True).order_by('batch').last()
        form_student = StudentForm(data={'user': user.id, 'training': training.id})
        if form_student.is_valid():
            form_student.save()

        return redirect("website:accounts:index")

    context = {
        'title': 'Lengkapi Profil Anda',
        'form': form
    }
    return render(request, 'accounts/index.html', context)


def login_view(request):
    next = request.GET.get('next') or None
    # form = AuthenticationForm(request, data=request.POST or None)
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        if next:
            return redirect(next)
        else:
            return redirect("website:accounts:index")

    context = {
        'form': form,
        'title': 'Masuk',
        'page': 'login'
    }
    return render(request, 'accounts/form.html', context)


def logout_view(request):
    logout(request)
    return redirect("website:index")


def sign_up(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tolong cek email Anda untuk mengaktifkan akun')
        return redirect('website:accounts:sign_up')

    context = {
        'form': form,
        'title': 'Daftar',
        'page': 'sign-up'
    }
    return render(request, 'accounts/form.html', context)


def active_account(request, uidb36, token):
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        login(request, user)
        messages.success(request, 'Selamat, akun Anda sudah aktif')
    else:
        messages.warning(request, 'Maaf, ada masalah dengan aktivasi akun')

    return redirect("website:accounts:index")

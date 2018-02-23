from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404

from academy.apps.accounts.models import User
from . forms import CustomAuthenticationForm, SignupForm, ProfileForm


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
        messages.success(request, 'Terima kasih telah melengkapi profil Anda')
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

def profile(request):
    user = request.user

    context = {
        'title' : 'Dashboard',
        'user'  : user,
    }
    return render(request, 'dashboard/profile.html', context)   

@login_required
def edit_profile(request):
    user = request.user

    initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone,
        'avatar': user.profile.avatar,
        'birthday': user.profile.birthday,
        'gender': user.profile.gender,
        'address': user.profile.address,
        'linkedin': user.profile.linkedin,
        'git_repo': user.profile.git_repo,
        'blog': user.profile.blog,
        'facebook':user.profile.facebook,
        'youtube': user.profile.youtube,
        'twitter': user.profile.twitter,
        'instagram': user.profile.instagram
    }

    form = ProfileForm(request.POST or None, request.FILES or None,
                          initial=initial, instance=user.profile)
    if form.is_valid():
        form.save(user)
        form.update_user(user)
        messages.success(request, 'Profil berhasil diubah')
        return redirect("website:accounts:profile")

    context = {
        'title': 'Ubah Profil',
        'form': form
    }
    return render(request, 'accounts/index.html', context)

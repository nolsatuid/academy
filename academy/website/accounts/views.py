from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import base36_to_int
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404

from academy.apps.accounts.models import User
from . forms import CustomAuthenticationForm, SignupForm


@login_required
def index(request):
    context = {
        'title': 'Account Index',
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
        'title': 'Log in',
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
        messages.success(request, 'Please check your email to activate your account')

    context = {
        'form': form,
        'title': 'Sign up',
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
        messages.success(request, 'Congratulation, your account is active')
    else:
        messages.warning(request, 'Sorry, there was a problem with account activation')

    return redirect("website:accounts:index")

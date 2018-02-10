from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
            return redirect("website:index")

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
        return redirect("website:index")

    context = {
        'form': form,
        'title': 'Sign up',
        'page': 'sign-up'
    }
    return render(request, 'accounts/form.html', context)

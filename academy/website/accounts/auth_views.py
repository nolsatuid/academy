from urllib import parse

from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from academy.website.accounts.forms import CustomAuthenticationForm

JWT_AUTH_HEADER_KEY = "X-User-Token"


def success_redirect(request):
    """
    Redirect utils when login success
    :param request:
    :return:
    """
    next = request.GET.get('next') or None
    if next:
        return redirect(next)
    else:
        return redirect("website:accounts:index")


def redirect_login(request):
    query = parse.urlencode(request.GET)
    response = redirect("website:accounts:login")
    response['Location'] += '?' + query
    return response


def login_form_view(request):
    """
    Standard Login Form
    :param request:
    :return:
    """
    navbar = request.GET.get('navbar')

    if request.user.is_authenticated:
        return success_redirect(request)

    form = CustomAuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return success_redirect(request)

    context = {
        'form': form,
        'title': 'Masuk',
        'page': 'login',
        'navbar': navbar,
        'mobile_layout': navbar
    }
    return render(request, 'accounts/form.html', context)


def jwt_header_login(request):
    """
    JWT Header Login Handler
    :param request:
    :return:
    """
    if JWT_AUTH_HEADER_KEY not in request.headers:
        return redirect_login(request)

    jwt_token = request.headers[JWT_AUTH_HEADER_KEY]
    try:
        token = AccessToken(jwt_token)
        user = JWTAuthentication().get_user(token)
        login(request, user, backend='academy.core.custom_auth.EmailBackend')
        return success_redirect(request)
    except (TokenError, AuthenticationFailed, InvalidToken):
        # Token invalid redirect to login page
        return redirect_login(request)


def login_view(request):
    """
    Main View For Login
    :param request:
    :return:
    """
    if JWT_AUTH_HEADER_KEY in request.headers:
        return jwt_header_login(request)

    return login_form_view(request)


def logout_view(request):
    """
    Main View For Logout
    :param request:
    :return:
    """
    logout(request)

    if 'next' in request.GET:
        return redirect(request.GET.get('next'))

    return redirect("website:index")

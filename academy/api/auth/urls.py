from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)

from . import views

app_name = "auth"
urlpatterns = [
    path('login', views.AuthLogin.as_view(), name="login"),
    path('token-refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('token-verify', TokenVerifyView.as_view(), name="token_verify"),
    path('register', views.RegisterView.as_view(), name="register"),
]

from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from . import views


app_name = "api"
urlpatterns = [
    path('auth/login', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token-refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('auth/token-verify', TokenVerifyView.as_view(), name="token_verify"),
    path('user/', include('academy.api.user.urls')),
    path('home', views.HomeView.as_view(), name="home"),
]

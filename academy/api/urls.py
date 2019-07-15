from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


app_name = "api"
urlpatterns = [
    path('auth/', include('academy.api.auth.urls')),
    path('user/', include('academy.api.user.urls')),
    path('infos/', include('academy.api.infos.urls')),
]

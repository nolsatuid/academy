from django.urls import path
from . import views

app_name = "devices"
urlpatterns = [
    path('', views.TokenFCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create'),
]

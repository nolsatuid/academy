from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path('profile', views.GetProfileView.as_view(), name='profile')
]

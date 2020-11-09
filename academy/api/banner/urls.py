from django.urls import path
from . import views

app_name = "banner"

urlpatterns = [
    path('', views.BannerListView.as_view(), name='banner'),
]

from django.urls import path
from . import views


app_name = "infos"
urlpatterns = [
    path('statistics', views.GetStatisticsView.as_view(), name='statistics'),
    path('logo/partners', views.GetLogoPartners.as_view(), name='logo-partners')
]

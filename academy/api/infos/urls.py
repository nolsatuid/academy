from django.urls import path
from . import views

app_name = "infos"
urlpatterns = [
    path('statistics', views.GetStatisticsView.as_view(), name='statistics'),
    path('logo/partners', views.GetLogoPartners.as_view(), name='logo-partners'),
    path('logo/sponsors', views.GetLogoSponsors.as_view(), name='logo-sponsors'),
    path('verify', views.VerifyCertificate.as_view(), name='verify-certificate'),
    path('instructors', views.GetInstructorsView.as_view(), name='instructors'),
    path('news', views.GetNewsView.as_view(), name='news'),
]

from django.urls import path, include
from django.conf.urls import handler404, handler500
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('error404/', views.error_404, name='error404'),
    path('error500/', views.error_500, name='error500'),
    path('faq/', views.faq, name='faq'),
    path('accounts/', include('academy.website.accounts.urls', namespace='accounts')),
    path('verify/', views.certificate_verify, name='cert-verify'),
    path('campuses/', include('academy.website.campuses.urls')),
    path('about/', views.about, name='about'),
    path('talent/', views.talent, name='talent'),
    path('company/', views.company, name='company'),
    path('statistic/', views.statistic, name='statistic'),
]

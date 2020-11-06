from django.urls import path, include
from django.conf.urls import handler404, handler500
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home_custom, name='index'),
    path('profile/', views.profile, name='profile'),
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
    path('blogs/<slug:slug>', views.blog_details, name='blog_details'),
    path('blogs/', views.blog_index, name='blog_index'),
    path('content/<slug:type_content>/<slug:slug>/',
         views.page_category, name='page_category'),
    path('content/<slug:type_content>/<slug:categoryslug>/<slug:slug>/',
         views.page_category_detail, name='page_category_detail'),
    path('contact/', views.contact, name='contact'),
]

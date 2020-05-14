from django.urls import path

from . import views

app_name = 'settings'

urlpatterns = [
    path('email', views.email_index, name='email_index'),
    path('email/edit/', views.email_edit, name='email_edit'),
    path('certificate-preview', views.certificate_preview, name='certificate_preview'),
]

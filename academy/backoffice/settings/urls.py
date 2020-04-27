from django.urls import path

from . import views

app_name = 'email'

urlpatterns = [
    path('email', views.email_index, name='email_index'),
    path('email/edit/', views.email_edit, name='email_edit'),
]

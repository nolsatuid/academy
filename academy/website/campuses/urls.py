from django.urls import path
from . import views

app_name = 'campuses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:campus_id>/register/', views.register, name='register'),
    path('<int:campus_id>/complate-profile/', views.complete_profile, name='complete_profile')
]

from django.urls import path
from . import views

app_name = 'trainings'

urlpatterns = [
    path('materials/', views.materials, name='materials'),
]

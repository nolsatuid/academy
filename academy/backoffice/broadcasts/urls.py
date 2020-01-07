from django.urls import path

from . import views

app_name = 'broadcasts'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('delete/<int:id>', views.delete, name='delete'),
]

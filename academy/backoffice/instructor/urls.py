from django.urls import path

from . import views

app_name = 'instructor'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('add/', views.add, name='add'),
    path('find-user/', views.ajax_find_user, name='ajax_find_user'),
]

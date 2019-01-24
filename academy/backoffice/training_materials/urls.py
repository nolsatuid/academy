from django.urls import path

from . import views

app_name = 'training_materials'

urlpatterns = [
    path(r'<int:id>/delete/', views.delete, name='delete'),
    path(r'<int:id>/edit/', views.edit, name='edit'),
    path(r'add/', views.add, name='add'),
    path(r'', views.index, name='index'),
    path(r'status/', views.bulk_material_status, name='bulk_material_status')
]

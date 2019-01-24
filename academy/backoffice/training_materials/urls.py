from django.urls import path

from . import views

app_name = 'training_materials'

urlpatterns = [
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('add/', views.add, name='add'),
    path('', views.index, name='index'),
    path('status/', views.bulk_material_status, name='bulk_material_status')
]

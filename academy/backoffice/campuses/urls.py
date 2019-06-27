from django.urls import path

from . import views

app_name = 'campuses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('add/', views.add, name='add'),
    path('details/<int:id>', views.details, name='details'),
    path('participants/', views.ParticipantsView.as_view(), name='participants'),
    path('users/selection/', views.UserSelectionView.as_view(), name='users_selection'),
]

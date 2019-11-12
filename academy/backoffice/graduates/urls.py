from django.urls import path

from . import views

app_name = 'graduates'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('candidates/', views.candidates, name='candidates'),
    path('candidate-to-graduates/<int:id>', views.candidate_to_graduates, name='candidate_to_graduates'),
    path('details/<int:id>', views.details, name='details'),
    path('participants-repeat/', views.participants_repeat, name='participants_repeat'),
    path('status-training/<int:id>/', views.status_training,
         name='status_training'),
    path('certificate/<int:id>/', views.show_certificate,
         name='show_certificate'),
    path('add-training-material/<int:id>/', views.add_training_material,
         name='add_training_material'),
    path('delete-training-status/<int:id>/<int:graduate_id>', views.delete_training_status,
         name='delete_training_status'),
    path('is-channeled', views.change_is_channeled, name='change_is_channeled'),
    path('add-rating/<int:id>/', views.add_rating,
         name='add_rating'),
]

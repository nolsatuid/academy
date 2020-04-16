from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
     path('', views.index, name='index'),
     path('<int:id>/', views.details, name='details'),
     path('participants/', views.participants, name='participants'),
     path('<int:id>/change-to/participant/', views.change_to_participant,
          name='change_to_participant'),
     path('<int:id>/change-to/pre-test/', views.change_to_pre_test,
          name='change_to_pre_test'),
     path('<int:id>/status-training/', views.status_training,
          name='status_training'),
     path('batch-training/', views.batch_training, name='batch_training'),
     path('batch-training/<int:id>/edit', views.edit_batch_training, name='edit_batch_training'),
     path('<int:student_id>/batch/', views.edit_student_batch,
          name='edit_student_batch'),
     path('<int:student_id>/status/', views.edit_status,
          name='edit_status'),
     path('last-login/', views.last_login, name='last_login'),
]

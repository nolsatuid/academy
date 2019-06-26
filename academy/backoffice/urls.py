from django.urls import path, include

from . import views


app_name = 'backoffice'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', include('academy.backoffice.users.urls', namespace='users')),
    path('training-materials/', include('academy.backoffice.training_materials.urls',
                                        namespace='training_materials')),
    path('graduates/', include('academy.backoffice.graduates.urls', namespace='graduates')),
    path('instructors/', include('academy.backoffice.instructor.urls', namespace='instructors')),
    path('surveys/', include('academy.backoffice.surveys.urls', namespace='surveys')),
    path('partners/', include('academy.backoffice.partner.urls', namespace='partners')),
    path('campuses/', include('academy.backoffice.campuses.urls', namespace='campuses')),
    path('sponsors/', include('academy.backoffice.sponsors.urls', namespace='sponsors')),
]

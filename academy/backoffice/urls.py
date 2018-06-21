from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/', include('academy.backoffice.users.urls', namespace='users')),
    url(r'^training-materials/', include('academy.backoffice.training_materials.urls',
                                         namespace='training_materials')),
    url(r'graduates/', include('academy.backoffice.graduates.urls', namespace='graduates')),
    url(r'instructors/', include('academy.backoffice.instructor.urls', namespace='instructors'))
]
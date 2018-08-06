from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>\d+)/$', views.details, name='details'),
    url(r'^participants/$', views.participants, name='participants'),
    url(r'^(?P<id>\d+)/change-to/participant/$', views.change_to_participant,
        name='change_to_participant'),
    url(r'^(?P<id>\d+)/status-training/$', views.status_training,
        name='status_training'),
    url(r'^batch-training/$', views.batch_training, name='batch_training'),
    url(r'^batch-training/(?P<id>\d+)/edit$', views.edit_batch_training, name='edit_batch_training'),
    url(r'^(?P<student_id>\d+)/batch/$', views.edit_student_batch,
        name='edit_student_batch'),
    url(r'^(?P<student_id>\d+)/status/$', views.edit_status,
        name='edit_status'),
]
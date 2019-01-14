from django.conf.urls import url

from . import views

app_name = 'graduates'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidates/$', views.candidates, name='candidates'),
    url(r'^candidate-to-graduates/(?P<id>\d+)$', views.candidate_to_graduates, name='candidate_to_graduates'),
    url(r'^details/(?P<id>\d+)$', views.details, name='details'),
    url(r'^participants-repeat/$', views.participants_repeat, name='participants_repeat'),
    url(r'^status-training/(?P<id>\d+)/$', views.status_training,
        name='status_training'),
    url(r'^certificate/(?P<id>\d+)/$', views.show_certificate,
        name='show_certificate'),
    url(r'^add-training-material/(?P<id>\d+)/$', views.add_training_material,
        name='add_training_material'),
    url(r'^delete-training-status/(?P<id>\d+)/(?P<graduate_id>\d+)$', views.delete_training_status,
        name='delete_training_status'),
]

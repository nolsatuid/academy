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
]
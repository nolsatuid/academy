from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidates/$', views.candidates, name='candidates'),
    url(r'^candidate-to-graduates/(?P<id>\d+)$', views.candidate_to_graduates, name='candidate_to_graduates'),
    url(r'^details/(?P<id>\d+)$', views.details, name='details'),
    url(r'^participants-repeat/$', views.participants_repeat, name='participants_repeat'),
]
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^add/$', views.add, name='add'),
    url(r'^$', views.index, name='index'),
    url(r'^status/$', views.bulk_training_status, name='bulk_training_status')
]
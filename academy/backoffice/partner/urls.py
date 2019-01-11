from django.conf.urls import url

from . import views

app_name = 'survey'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<id>\d+)/edit/$', views.edit, name='edit'),
    url(r'(?P<id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^add/$', views.add, name='add'),
]

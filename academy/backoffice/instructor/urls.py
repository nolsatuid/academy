from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^add/$', views.add, name='add'),
    url(r'^find-user/$', views.ajax_find_user, name='ajax_find_user'),
]
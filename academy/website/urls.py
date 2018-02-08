from django.conf.urls import url, include, handler404, handler500

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
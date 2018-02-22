from django.conf.urls import url, include, handler404, handler500

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^tilil/', views.tilil, name='tilil'),
    url(r'^accounts/', include('academy.website.accounts.urls', namespace='accounts')),
]
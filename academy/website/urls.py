from django.conf.urls import url, include, handler404, handler500

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^error404/', views.error_404, name='error404'),
    url(r'^error500/', views.error_500, name='error500'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^accounts/', include('academy.website.accounts.urls', namespace='accounts')),
]
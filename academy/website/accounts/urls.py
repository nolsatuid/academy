from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^sign-up/$', views.sign_up, name='sign_up'),
    url(r'^activate/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$',
        views.active_account, name='active_account'),
]
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^sign-up/$', views.sign_up, name='sign_up'),
    url(r'^activate/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$',
        views.active_account, name='active_account'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^forgot-password/$', views.forgot_password, name='forgot_password'),
    url(r'^reset-password/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$',
        views.reset_password, name='reset_password'),
    url(r'^trainings/', include('academy.website.accounts.trainings.urls', namespace='trainings')),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^survey/edit/$', views.edit_survey, name='edit_survey')
]
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^materials/$', views.materials, name='materials'),
]
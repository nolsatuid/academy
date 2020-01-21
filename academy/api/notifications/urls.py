from django.urls import path
from . import views

app_name = "notifications"
urlpatterns = [
    path('inbox', views.SendNotification.as_view(), name='send_notification'),
]

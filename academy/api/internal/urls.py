from django.urls import path
from . import views

app_name = "internal"
urlpatterns = [
    path('demo/', views.DemoView.as_view(), name='demo'),
    path('generate-certificate/', views.GenerateCertificateView.as_view(),
         name='generate_certificate'),
    path('user/<int:user_id>', views.UserView.as_view(), name='user'),
    path('notification', views.SendNotification.as_view(), name='notification'),
    path('regenerate-certificate/<int:user_id>', views.RegenerateCertificateView.as_view(), name='regenerate_certificate'),
    path('get-user', views.GetUserView.as_view(), name='get_user'),
]

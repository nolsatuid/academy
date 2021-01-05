from django.urls import path
from . import views

app_name = "certificate"
urlpatterns = [
    path('', views.CertificateListView.as_view(), name='certificate_list'),
    path('<int:id>', views.CertificateDetailView.as_view(), name='certificate_detail'),
]

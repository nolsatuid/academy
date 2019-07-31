from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path('profile', views.GetProfileView.as_view(), name='profile'),
    path('upload/cv', views.UploadCV.as_view(), name='upload_cv'),
    path('survey', views.SurveyView.as_view(), name='survey'),
]

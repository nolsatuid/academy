from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('upload/cv', views.UploadCVView.as_view(), name='upload_cv'),
    path('survey', views.SurveyView.as_view(), name='survey'),
    path('upload/avatar', views.UploadAvatarView.as_view(), name='upload_avatar'),
    path('materials', views.MaterialsView.as_view(), name='materials'),
    path('graduate', views.GetGraduateView.as_view(), name='graduate'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
]

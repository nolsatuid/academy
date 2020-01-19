from django.urls import path, include

app_name = "api"
urlpatterns = [
    path('auth/', include('academy.api.auth.urls')),
    path('user/', include('academy.api.user.urls')),
    path('infos/', include('academy.api.infos.urls')),
    path('inbox/', include('academy.api.inbox.urls')),
    path('notifications/', include('academy.api.notifications.urls')),
    path('devices/', include('academy.api.devices.urls'))
]

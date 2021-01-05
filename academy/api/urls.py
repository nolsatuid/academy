from django.urls import path, include

app_name = "api"
urlpatterns = [
    path('', include('academy.api.gateway.urls')),
    path('auth/', include('academy.api.auth.urls')),
    path('user/', include('academy.api.user.urls')),
    path('infos/', include('academy.api.infos.urls')),
    path('inbox/', include('academy.api.inbox.urls')),
    path('devices/', include('academy.api.devices.urls')),
    path('banners/', include('academy.api.banner.urls')),
    path('certificates/', include('academy.api.certificate.urls')),
    path('internal/', include('academy.api.internal.urls'))
]

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from academy.api.authentications import APISessionAuthentication


class TokenFCMDeviceAuthorizedViewSet(FCMDeviceAuthorizedViewSet):
    authentication_classes = (JWTAuthentication, APISessionAuthentication)

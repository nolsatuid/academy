import datetime

import jwt
import requests
from django.conf import settings
from django.urls import path
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_server_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }, settings.SECRET_KEY)


def gate_func(remote_base):
    @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
    @authentication_classes([JWTAuthentication])
    @permission_classes([AllowAny])
    def func(req, remote_path):
        url = remote_base + remote_path
        method = req.method.lower()
        data = req.data
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }
        user_id = req.user.id if req.user and req.user.is_authenticated else None

        headers = {
            'authorization': f'Server {get_server_token(user_id)}'
        }

        res = method_map[method](url, headers=headers, data=data, files=req.FILES)

        if res.headers.get('Content-Type', '').lower() == 'application/json':
            data = res.json()
        else:
            data = res.content
        return Response(data=data, status=res.status_code)

    return func


def gate(api_path, remote_base):
    return path(api_path + '/<path:remote_path>', gate_func(remote_base))

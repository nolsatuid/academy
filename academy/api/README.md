# API

## Login
url: `/api/auth/login`

header:
```
Conten-Type application/json
```

method: `POST`

body:
```json
{
    "email": "youremail@example.com",
    "password": "acjd1123"
}
```

response:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU2MjIwNDkyOCwianRpIjoiMzFlMGY4ZDE5ZDEzNDQwNmIzODA1M2Y4MWZlY2Q1YWIiLCJ1c2VyX2lkIjozfQ.TQXXRcjjaThOSE4P-4_IhGfz5X5xiNkDFIQjb",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTYyMTE4ODI4LCJqdGkiOiJhNDAzZGQwMzhjOWU0NzM5OGZlNjE4Y2JkMzQwZTQ0NyIsInVzZXJfaWQiOjN9.gwk0mwg9r4xejoMBNlax9rztmyUh9MaoCyGOGr"
}
```

## Refresh Token
url: `/api/auth/token-refresh`

header:
```
Conten-Type application/json
```

method: `POST`

body:
```json
{
    "refresh": "{your token access get after login}",
}
```

response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTYyMTE4ODI4LCJqdGkiOiJhNDAzZGQwMzhjOWU0NzM5OGZlNjE4Y2JkMzQwZTQ0NyIsInVzZXJfaWQiOjN9.gwk0mwg9r4xejoMBNlax9rztmyUh9MaoCyGOGr"
}
```
detail package (drf simplejwt) can see [in here](https://github.com/davesque/django-rest-framework-simplejwt)

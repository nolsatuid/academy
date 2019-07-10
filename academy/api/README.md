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

## Register
url: `/api/auth/register`

header:
```
Conten-Type application/json
```

method: `POST`

body:
```json
{
	"email": "irfan@btech.id",
	"username": "irfanpule",
	"password1": "kkajs1345",
	"password2": "kkajs1345"
}
```

response:
```json
{
    "message": "Mohon cek email lutfi@gmail.com Anda untuk mengaktifkan akun"
}
```

## Refresh Token
url: `/api/auth/token-refresh`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
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

## Get Profile
url: `/api/user/profile`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response:
```json
{
    "name": "Muhammad Irfan",
    "username": "irfanpule",
    "email": "irfanpule@btech.id",
    "phone": "08978950954",
    "is_active": true,
    "avatar": null,
    "linkedin": "",
    "git_repo": "https://github.com/irfanpule",
    "blog": "",
    "facebook": "",
    "youtube": "",
    "twitter": "",
    "instagram": "irfanpule",
    "telegram_id": "",
    "curriculum_vitae": "http://localhost:8000/media/files/cv/2019/07/10/template_cv_nolsatu.docx",
    "has_profile": true
}
```

## Edit Profile
url: `/api/user/profile`

header:
```
Conten-Type multipart/form-data
Authorization Bearer {token access}
```

method: `POST`

body: `form-data`
```
name = "Muhammad Irfan"
username = "irfanpule"
phone = "08978950954"
linkedin = ""
git_repo = "https://github.com/irfanpule"
blog = ""
facebook = ""
youtube = ""
twitter = ""
instagram = "irfanpule"
telegram_id = ""
curriculum_vitae = template_cv_nolsatu.docx
```

response:
```json
{
    "name": "Muhammad Irfan",
    "username": "irfanpule",
    "email": "irfanpule@btech.id",
    "phone": "08978950954",
    "is_active": true,
    "avatar": null,
    "linkedin": "",
    "git_repo": "https://github.com/irfanpule",
    "blog": "",
    "facebook": "",
    "youtube": "",
    "twitter": "",
    "instagram": "irfanpule",
    "telegram_id": "",
    "curriculum_vitae": "http://localhost:8000/media/files/cv/2019/07/10/template_cv_nolsatu.docx",
    "has_profile": true
}
```

## Get Logo Partners
url: `/api/infos/logo/partners`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response:
```json
[
    {
        "name": "BINAR ACADEMY",
        "image": "https://www.nolsatu.id/media/images/partners/binar_3bvDd3s.png",
        "display_order": 1,
        "website": "https://binar.co.id/"
    }
]
```

## Get Logo Sponsors
url: `/api/infos/logo/sponsors`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response:
```json
[
    {
        "name": "BIZET GIO CLOUD",
        "image": "https://www.nolsatu.id/media/images/sponsors/biznet_gio_.png",
        "display_order": 1,
        "website": "https://www.biznetgio.com/"
    }
]
```
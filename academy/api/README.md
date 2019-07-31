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
    "username": "{email or username}",
    "password": "acjd1123"
}
```

response:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU2Mzc4NzY3OCwianRpIjoiMjY5NjczM2NmYzQ4NDU2Y2I0MzI2NjZhMTViZGJlMTIiLCJ1c2VyX2lkIjo1fQ.yK06YE03iaortWQ3KumhAQMDomU3RLbQF4qN2ir9zcw",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTYzNDQyMDc4LCJqdGkiOiIzNWM0OGVmNTFhYjY0Njc4OTJhMGViODBkZmJmOGVmMSIsInVzZXJfaWQiOjV9.yJk6jz-ijZVEq6NbLVYB2BxbB3izwzCnNv_mwnWrA4Y",
    "user": {
        "name": "Muhammad Lutfi",
        "username": "lutfi",
        "email": "lutfi@gmail.com",
        "phone": "08978950954",
        "is_active": true,
        "avatar": null,
        "linkedin": "",
        "git_repo": "",
        "blog": "",
        "facebook": "",
        "youtube": "",
        "twitter": "",
        "instagram": "",
        "telegram_id": "",
        "curriculum_vitae": "",
        "has_profile": false
    }
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
    "refresh": "{your token access get after login}"
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
Conten-Type application/json
Authorization Bearer {token access}
```

method: `POST`

body:
```
{
	"first_name": "Muhammad",
	"last_name": "Irfan",
	"phone_number": "08978950954",
	"linkedin": "",
	"git_repo": "https://github.com/irfanpule",
	"blog": "",
	"youtube": "",
	"facebook": "",
	"instagram": "irfanpule",
	"twitter": "",
	"telegram_id": ""
}
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
    "curriculum_vitae": null,
    "has_profile": true
}
```

## Upload CV
url: `/api/user/upload/cv`

header:
```
Conten-Type multipart/form-data
Authorization Bearer {token access}
```

method: `POST`

body:
```
curriculum_vitae = {file}
```

response: user payload
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
    "curriculum_vitae": "https://nolsatu.id/media/files/cv/2019/07/22/template_cv_nolsatu_QYHIHvA.docx",
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

## Get statistics
url: `/api/infos/statistics`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response:
```json
{
    "registrants": 3,
    "users": 3,
    "participants": 2,
    "graduates": 0,
    "channeled": 0
}
```

## Get Survey Answer
url: `/api/user/survey`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response (data survey tersedia):
```json
{
    "data": {
        "working_status": 1,
        "working_status_other": "",
        "graduate_channeled": false,
        "graduate_channeled_when": 1,
        "graduate_channeled_when_other": "",
        "channeled_location": [
            "Jakarta"
        ],
        "channeled_location_other": ["Blabla", "Bla"]
    }
}
```

response (data survey tidak tersedia):
```json
{
    "data": null
}
```

Mapping dan value yang tersedia untuk beberapa property

```
working_status:
    1 = employee/Karyawan
    2 = student/Mahasiswa
    3 = unemployed/Belum Bekerja
    99 = other/Lain-lain

graduate_channeled_when:
    1 = soon/Segera,
    99 = other/Lain-lain

channeled_location = [
    'Jakarta',
    'Yogyakarta', 
    'Bandung',
    'Lain-lain'
]
```

## Isi Survey
url: `/api/user/survey`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `POST`

request:
```json
{
	"working_status": 99,
	"working_status_other": "Nganggur",
	"graduate_channeled": true,
	"graduate_channeled_when": 99,
	"graduate_channeled_when_other": "Kapan Aja",
	"channeled_location": [
	    "Jakarta",
	    "Lain-lain"
	],
	"channeled_location_other": "Zimbabwe,Kuvukiland"
}
```

response:
```json
{
    "data": {
        "working_status": 99,
        "working_status_other": "Nganggur",
        "graduate_channeled": true,
        "graduate_channeled_when": 99,
        "graduate_channeled_when_other": "Kapan Aja",
        "channeled_location": [
            "Jakarta",
            "Lain-lain"
        ],
        "channeled_location_other": [
            "Zimbabwe",
            "Kuvukiland"
        ]
    }
}
```

Mapping dan value yang tersedia untuk beberapa property dapat dilihat diatas.

Karena form yang digunakan sama dengan yang ada di web, maka ada beberapa aturan yang harus di ikuti:

1. `channeled_location_other` adalah string yang dipisahkan dengan koma
2. `channeled_location_other` tidak akan disimpan jika dalam `channeled_location` tidak ada `Lain-lain`


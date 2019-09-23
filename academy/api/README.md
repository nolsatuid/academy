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
`has_profile` digunakan untuk mengetahui apakah user tersebut sudah memiliki data `profile`, jika false maka tampilkan form lengkapi profil

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
    "status": 1,
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

Mapping dan value yang tersedia untuk status user

```
status:
    1 = seleksi
    2 = peserta
    3 = mengulang
    4 = lulus
```


## Upload Avatar
url: `/api/user/upload/avatar`

header:
```
Conten-Type multipart/form-data
Authorization Bearer {token access}
```

method: `POST`

body:
```
avatar = {file}
```

response: user payload
```json
{
    "name": "Muhammad Irfan",
    "username": "irfanpule",
    "email": "irfanpule@btech.id",
    "phone": "08978950954",
    "is_active": true,
    "status": 1,
    "avatar": "http://localhost:8000/media/images/avatar/2019/07/31/avatar-wanita.png",
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
{
    "data":[
        {
            "name": "BINAR ACADEMY",
            "image": "https://www.nolsatu.id/media/images/partners/binar_3bvDd3s.png",
            "display_order": 1,
            "website": "https://binar.co.id/"
        }
    ]
}
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
{
    "data":[
        {
            "name": "BIZET GIO CLOUD",
            "image": "https://www.nolsatu.id/media/images/sponsors/biznet_gio_.png",
            "display_order": 1,
            "website": "https://www.biznetgio.com/"
        }
    ]
}
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


## Get Training Material
url: `/api/user/materials`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response:
```json
{
    "data": [
        {
            "code": "OSB",
            "title": "OpenStack Beginner",
            "status": "Lulus"
        },
        {
            "code": "DO",
            "title": "Docker",
            "status": "Belum"
        }
    ]
}
```
## API Change Password
url: `/api/user/change-password`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `POST`

body:
```json
{
    "old_password": "{old password}",
    "new_password1": "{new password}",
    "new_password2": "{confirm new password}"
}
```

response:
```json
{
    "message": "Password berhasil diubah"
}
```
## Verify Certificate
url: `/api/infos/verify`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `POST`

request:
```json
{
	"certificate_number": "NS-0105-2019-0822",
	"last_name": "Nugroho"
}
```

response:
```json
{
    "full_name": "Setyo Nugroho",
    "certificate_number": "NS-0105-2019-0822",
    "issued_at": "22 Aug 2019",
    "valid_until": "21 Aug 2022"
}
```

certificate not found error (http status 400):

```json
{
    "detail": "Your request cannot be completed",
    "error_message": "Maaf, kami tidak dapat menemukan sertifikat dengan nomor sertifikat dan nama belakang tersebut.",
    "error_code": "invalid_request"
}
```

## Get Instructors
url: `/api/infos/instructors`

method: `GET`

response:
```json
{
    "data": [
        {
            "name": "Utian Ayuba",
            "specialization": "IaaS Cloud Architect",
            "linkedin": "https://www.linkedin.com/in/utianayuba/"
        }
    ]
}
```
## Get Graduate
url: `/api/user/graduate`

header:
```
Conten-Type application/json
Authorization Bearer {token access}
```

method: `GET`

response:
```json
{
    "data": {
        "certificate_url": "http://127.0.0.1:8000/media/images/certificates/2019/01/24/certificate-muhammad-hanif.pdf",
        "certificate_number": "NS-0022-2018-0603",
        "is_channeled": true,
        "channeled_at": "tes"
    }
}
```

## Get News
url: `/api/infos/news`

header:
```
Conten-Type application/json
```

method: `GET`

```json
{
    "data": [
        {
            "source_name": "Linuxtoday.com",
            "source_link": "https://www.linuxtoday.com/",
            "source_identifier": "linux_today",
            "post_title": "Manjaro 18.1: Goes Arch One Better",
            "post_link": "http://feedproxy.google.com/~r/LinuxToday/~3/pTuZ32M08zs/manjaro-18.1-goes-arch-one-better.html"
        },
    ]
}
```

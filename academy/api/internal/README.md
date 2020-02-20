# API Internal

## Generate Certificate
url: `/api/internal/generate-certificate`

header:
```
Conten-Type application/json
```

method: `POST`

body:
```json
{
    "title": "Python Basic",
    "certificate_number": "NS-DEV-00001-0001",
    "user_id": 12,
    "created": "20-02-2020"
}
```

response:
```json
{
    "id": 1,
    "title": "Python Basic",
    "number": "NS-DEV-00001-0001",
    "user": 12,
    "certificate_file": "/media/images/certificates/2020/02/20/certificate-irfan-btech.pdf",
    "created": "2020-02-20T00:00:00Z"
}
```

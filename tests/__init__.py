from django.test import TestCase
from academy.apps.offices.models import Setting, AuthSetting, ConfigEmail


class AcademyTestCase(TestCase):

    def setUp(self):
        Setting.objects.create()
        AuthSetting.objects.create()
        ConfigEmail.objects.update_or_create(
            id=1,
            from_email="no-reply@example.id",
            email_host="mail.example.id",
            email_user="no-reply@example.id",
            email_password="Password123",
            email_port=587,
            use_tls=False,
            recipient_email="no-reply@example.id"
        )

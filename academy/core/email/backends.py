from django.core.mail.backends import smtp

from academy.apps.offices.models import ConfigEmail


class AcademySMTPEmailBackend(smtp.EmailBackend):
    def __init__(self, **kwargs):
        email_config = ConfigEmail.objects.get(id=1)
        kwargs['host'] = email_config.email_host
        kwargs['port'] = email_config.email_port
        kwargs['username'] = email_config.email_user
        kwargs['password'] = email_config.email_password
        kwargs['use_tls'] = email_config.use_tls

        super().__init__(**kwargs)

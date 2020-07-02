import django_rq
from django import forms
from post_office import mail

from academy.apps.offices.models import ConfigEmail
from academy.core.email_utils import construct_email_args


class ConfigEmailForm(forms.ModelForm):
    class Meta:
        model = ConfigEmail
        exclude = []


class TestEmailForm(forms.Form):
    email_to = forms.EmailField(label="Penerima")
    message = forms.CharField(widget=forms.Textarea, label="Pesan")

    def send_email(self):
        mail.send(
            [self.cleaned_data['email_to']],
            subject="Test Email",
            message=self.cleaned_data['message'],
            priority='now',
        )
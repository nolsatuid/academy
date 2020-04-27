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
    email_to = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        kwargs = construct_email_args(
            recipients=[self.cleaned_data['email_to']],
            subject="Test Email",
            content=self.cleaned_data['message']
        )
        django_rq.enqueue(mail.send, **kwargs)
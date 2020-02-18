from django import forms
from academy.apps.accounts.models import User, Certificate


class GenerateCertificateForm(forms.Form):
    title = forms.CharField()
    certificate_number = forms.CharField()
    user_id = forms.ModelChoiceField(queryset=User.objects.all())
    created = forms.DateTimeField(input_formats=['%d-%m-%Y'], required=False)

    def save(self):
        cleaned_data = super().clean()
        cert = Certificate.objects.create(
            title=cleaned_data["title"],
            number=cleaned_data["certificate_number"],
            user=cleaned_data["user_id"]
        )
        if cleaned_data["created"]:
            cert.created = cleaned_data["created"]
            cert.save()
        cert.generate()
        return cert

from django import forms

from academy.apps.accounts.models import Certificate
from academy.apps.graduates.models import Graduate


class CertificateVerifyForm(forms.Form):
    certificate_number = forms.CharField(
        label='Nomor Sertifikat', max_length=35,
        widget=forms.TextInput(attrs={'placeholder': 'ex: NS-XXXXX-XXXX-XXXX'})
    )
    last_name = forms.CharField(label='Nama Belakang',
                                help_text="Nama Belakang harus sesuai dengan yang tertetera pada profil Anda.")

    def get_certificate(self, certificate_number, last_name):
        certificate = Certificate.objects.filter(
            number__iexact=certificate_number
        ).select_related('user').last()

        if certificate and certificate.is_name_valid(last_name):
            return {
                "user": {
                    "full_name": certificate.user.get_full_name(),
                    "first_name": certificate.user.first_name,
                    "last_name": certificate.user.last_name
                },
                "certificate_number": certificate.number,
                "created": certificate.created,
                "valid_until": certificate.valid_until
            }

        return None

    def get_graduate(self, certificate_number, last_name):
        graduate = Graduate.objects.filter(
            certificate_number__iexact=certificate_number
        ).select_related('user').last()

        if graduate and graduate.is_name_valid(last_name):
            return {
                "user": {
                    "full_name": graduate.user.get_full_name(),
                    "first_name": graduate.user.first_name,
                    "last_name": graduate.user.last_name
                },
                "certificate_number": graduate.certificate_number,
                "created": graduate.created,
                "valid_until": graduate.valid_until,
                "rating_stars": graduate.get_rating_stars(None),
                "rating_accumulation": graduate.rating_accumulation(),
                "rating_respondents": graduate.ratings.count()
            }

        return None

    def verification(self, *args, **kwargs):
        certificate_number = self.cleaned_data['certificate_number']
        last_name = self.cleaned_data['last_name']

        if "DEV" in certificate_number:
            return self.get_certificate(certificate_number, last_name)
        else:
            return self.get_graduate(certificate_number, last_name)

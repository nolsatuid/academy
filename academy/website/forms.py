from django import forms

from academy.apps.graduates.models import Graduate


class CertificateVerifyForm(forms.Form):
    certificate_number = forms.CharField(
        label='Nomor Sertifikat', max_length=35,
        widget=forms.TextInput(attrs={'placeholder': 'ex: NS-XXXXX-XXXX-XXXX'})
    )
    last_name = forms.CharField(label='Nama Belakang', help_text="Nama Belakang harus sesuai dengan yang tertetera pada profil Anda.")

    def verification(self, *args, **kwargs):
        certificate_number = self.cleaned_data['certificate_number']
        last_name = self.cleaned_data['last_name']
        graduates = Graduate.objects.filter(
            certificate_number__iexact=certificate_number
        ).select_related('user').last()

        if graduates:
            if (
                graduates.user.last_name and graduates.user.last_name.lower()
                == last_name.lower()
            ) or (
                not graduates.user.last_name and graduates.user.first_name and
                graduates.user.first_name.lower() == last_name.lower()
            ):
                return graduates
            else:
                return None

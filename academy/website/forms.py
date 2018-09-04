from django import forms

from academy.apps.graduates.models import Graduate


class CertificateVerifyForm(forms.Form):
    certificate_number = forms.CharField(label='Nomor Sertifikat', max_length=18,
                                widget=forms.TextInput(attrs={'placeholder': 'ex: NS-XXXXX-XXXX-XXXX'}))
    last_name = forms.CharField(label='Nama Belakang pada Sertifikat')

    def verification(self, *args, **kwargs):
        certificate_number = self.cleaned_data['certificate_number']
        last_name = self.cleaned_data['last_name']        
        student = Graduate.objects.filter(certificate_number__iexact=certificate_number).select_related('user')
        if student:
            if student.last().user.last_name:
                student = student.filter(user__last_name__iexact=last_name)
            else:
                student = student.filter(user__first_name__iexact=last_name)

        return student.last()

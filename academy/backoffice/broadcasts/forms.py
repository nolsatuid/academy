from django import forms

from academy.apps.broadcasts.models import Broadcast


class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ('__all__')

    def clean(self):
        cleaned_data = super().clean()
        if 'sms' in cleaned_data['via'] or 'SMS' in cleaned_data['via']:
            self.add_error('via', "Broadcast via SMS belum tersedia untuk saat ini.")

        return cleaned_data

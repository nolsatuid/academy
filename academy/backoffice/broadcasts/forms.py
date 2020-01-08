from django import forms

from academy.apps.broadcasts.models import Broadcast


class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ('__all__')

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('title'):
            raise forms.ValidationError("Title tidak boleh kosong")
        if not cleaned_data.get('via'):
            raise forms.ValidationError("Pilih via minimal satu")

        if 'push_notification' in cleaned_data['via'] or 'sms' in cleaned_data['via']:
            if not cleaned_data.get('short_content'):
                self.add_error('short_content', "Short Konten tidak boleh kosong")

        if 'email' in cleaned_data['via']:
            if not cleaned_data.get('html_content'):
                self.add_error('html_content', "HTML Konten tidak boleh kosong")

        if 'sms' in cleaned_data['via'] or 'SMS' in cleaned_data['via']:
            self.add_error('via', "Broadcast via SMS belum tersedia untuk saat ini.")

        return cleaned_data

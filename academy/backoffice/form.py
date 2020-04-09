from django import forms

from academy.apps.offices.models import Setting


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = ('name',)

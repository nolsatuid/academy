from django import forms

from academy.apps.campuses.models import Campus


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ['name', 'logo', 'description', 'address', 'email', 'phone', 'open_registration']

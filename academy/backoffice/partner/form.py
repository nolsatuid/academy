from django import forms

from academy.apps.offices.models import LogoPartner


class PartnerForm(forms.ModelForm):
    class Meta:
        model = LogoPartner
        fields = ['name', 'image', 'display_order', 'is_visible', 'website']

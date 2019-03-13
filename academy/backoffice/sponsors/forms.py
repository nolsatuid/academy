from django import forms

from academy.apps.offices.models import LogoSponsor


class SponsorForm(forms.ModelForm):
    class Meta:
        model = LogoSponsor
        fields = ['name', 'image', 'display_order', 'is_visible', 'website']


from django import forms

from academy.apps.accounts.models import Inbox


class AddInboxForm(forms.ModelForm):
    class Meta:
        model = Inbox
        fields = ('user', 'subject', 'content')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

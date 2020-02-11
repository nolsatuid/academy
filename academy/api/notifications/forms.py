from django import forms

from academy.apps.accounts.models import Inbox


class AddInboxForm(forms.ModelForm):
    class Meta:
        model = Inbox
        fields = ('user', 'subject', 'content', 'raw_content')

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['raw_content']:
            cleaned_data['raw_content'] = cleaned_data['content']
        return cleaned_data

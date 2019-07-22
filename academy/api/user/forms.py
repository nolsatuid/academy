from django import forms
from academy.core import fields
from academy.apps.accounts.models import Profile


class UploadCVForm(forms.ModelForm):
    curriculum_vitae = fields.FileFieldExtended(
        label='Curriculum Vitae',
        help_text="File Type: .doc, .docx. Max 2 MB. Mohon gunakan template yang disediakan",
        max_mb_file_size=2,
        allowed_content_type=[
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ]
    )

    class Meta:
        model = Profile
        fields = ('curriculum_vitae',)

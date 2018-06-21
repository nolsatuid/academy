from django import forms


class InitialPreviewFileInput(forms.ClearableFileInput):
    template_name = 'forms/widget/image_preview_file_input.html'

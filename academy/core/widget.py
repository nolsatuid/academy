from django import forms


class ImagePreviewFileInput(forms.ClearableFileInput):
    template_name = 'forms/widget/image_preview_file_input.html'


class AjaxSelect(forms.Select):
    template_name = 'forms/widget/ajax_select.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.placeholder = ""

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['url'] = self.url
        context['widget']['placeholder'] = self.placeholder
        return context

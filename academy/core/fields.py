from django import forms
from django.core.exceptions import ValidationError
from academy.apps.students.models import TrainingMaterial
from academy.core.widget import AjaxSelect
import magic


class AjaxModelChoiceField(forms.ChoiceField):
    """ An Ajax choice field that can get model from which item is selected
    Ajax response must at least have:
    data: [
        {
            id: 1,
            text: "Foo"
        }
    ]
    """
    widget = AjaxSelect()

    def __init__(self, model, url, placeholder="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.url = url
        self.widget.url = self.url
        self.widget.placeholder = placeholder

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            value = self.model.objects.get(pk=value)
        except (ValueError, TypeError, self.model.DoesNotExist):
            raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
        return value

    def valid_value(self, value):
        return True


class FileFieldExtended(forms.FileField):
    def __init__(self, allowed_content_type=None, max_mb_file_size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_content_type = allowed_content_type
        self.max_mb_file_size = max_mb_file_size

    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return None

        if self.max_mb_file_size and f.size > self.max_mb_file_size * 1048576:
            raise forms.ValidationError('Ukuran file maksimal 2 MB')

        if self.allowed_content_type and magic.from_buffer(f.read(), mime=True) not in self.allowed_content_type:
            raise forms.ValidationError('Tipe file tidak diperbolehkan')

        return f


class TrainingMaterialField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(queryset=TrainingMaterial.objects.all(), *args, **kwargs)

    def label_from_instance(self, obj):
        return f"{obj.code} - {obj.title}"

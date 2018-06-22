from django import forms
from django.core.exceptions import ValidationError

from academy.core.widget import AjaxSelect


class AjaxModelChoiceField(forms.ChoiceField):
    """ An Ajax choice field that can get model from which item is selected
    Ajax response must follow:
    data: [
        {
            id: 1,
            text: "Foo"
        }
    ]
    """
    widget = AjaxSelect()

    def __init__(self, model, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.url = url
        self.widget.url = self.url

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

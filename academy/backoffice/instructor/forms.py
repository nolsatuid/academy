from django import forms
from django.core.exceptions import ValidationError

from academy.apps.accounts.models import User
from academy.core.widget import InitialPreviewFileInput


# Need better name for this class
class AltModelChoiceField(forms.ChoiceField):
    def __init__(self, model, *args, **kwargs):
        super(AltModelChoiceField, self).__init__(*args, **kwargs)
        self.model = model

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


class BaseInstructorForm(forms.Form):
    first_name = forms.CharField(label='Nama Awal', required=True)
    last_name = forms.CharField(label='Nama Akhir', required=True)
    specialization = forms.CharField(label='Spesialisasi', required=True)
    avatar = forms.ImageField(label='Avatar', required=True, widget=InitialPreviewFileInput)

    def save(self, instructor=None):
        if instructor is not None:
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            specialization = self.cleaned_data['specialization']
            avatar = self.cleaned_data['avatar']

            instructor.role = User.ROLE.trainer
            instructor.first_name = first_name
            instructor.last_name = last_name
            instructor.profile.specialization = specialization
            instructor.profile.avatar = avatar
            instructor.save()
            instructor.profile.save()


class AddInstructorForm(BaseInstructorForm):
    instructor = AltModelChoiceField(model=User, required=True, label='Instruktur')

    field_order = ['instructor']

    def save(self, instructor=None):
        instructor = self.cleaned_data['instructor']

        super(AddInstructorForm, self).save(instructor)


class EditInstructorForm(BaseInstructorForm):
    instructor = forms.CharField(disabled=True)
    field_order = ['instructor']

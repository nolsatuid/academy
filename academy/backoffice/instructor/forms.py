from django import forms
from django.urls import reverse_lazy

from academy.apps.accounts.models import User
from academy.core.fields import AjaxModelChoiceField
from academy.core.widget import ImagePreviewFileInput


# Need better name for this class


class BaseInstructorForm(forms.Form):
    first_name = forms.CharField(label='Nama Awal', required=True)
    last_name = forms.CharField(label='Nama Akhir', required=True)
    specialization = forms.CharField(label='Spesialisasi', required=True)
    avatar = forms.ImageField(label='Avatar', required=True, widget=ImagePreviewFileInput)

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
    instructor = AjaxModelChoiceField(model=User, required=True,
                                      url=reverse_lazy('backoffice:instructors:ajax_find_user'),
                                      label='Instruktur')

    field_order = ['instructor']

    def save(self, instructor=None):
        instructor = self.cleaned_data['instructor']

        super().save(instructor)


class EditInstructorForm(BaseInstructorForm):
    instructor = forms.CharField(disabled=True)
    field_order = ['instructor']

from django import forms
from django.urls import reverse_lazy

from academy.apps.accounts.models import User, Profile
from academy.core.fields import AjaxModelChoiceField
from academy.core.widget import ImagePreviewFileInput


class BaseInstructorForm(forms.Form):
    first_name = forms.CharField(label='Nama Awal', required=True)
    last_name = forms.CharField(label='Nama Akhir', required=True)
    linked_in = forms.CharField(label='LinkedIn', required=True)
    specialization = forms.CharField(label='Spesialisasi', required=True)
    avatar = forms.ImageField(label='Avatar', required=True, widget=ImagePreviewFileInput)

    def save(self, instructor=None):
        if instructor:
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            linked_in = self.cleaned_data['linked_in']
            specialization = self.cleaned_data['specialization']
            avatar = self.cleaned_data['avatar']

            instructor.role = User.ROLE.trainer
            instructor.first_name = first_name
            instructor.last_name = last_name
            instructor.save()

            if hasattr(instructor, 'profile'):
                instructor.profile.specialization = specialization
                instructor.profile.avatar = avatar
                instructor.profile.linkedin = linked_in
                instructor.profile.save()
            else:
                profile = Profile(specialization=specialization, avatar=avatar, linkedin=linked_in, user=instructor)
                profile.save()


class AddInstructorForm(BaseInstructorForm):
    instructor = AjaxModelChoiceField(model=User, required=True,
                                      url=reverse_lazy('backoffice:instructors:ajax_find_user'),
                                      label='Instruktur')

    field_order = ['instructor']

    def save(self, *args, **kwargs):
        instructor = self.cleaned_data['instructor']

        super().save(instructor=instructor)


class EditInstructorForm(BaseInstructorForm):
    instructor = forms.CharField(disabled=True)
    field_order = ['instructor']

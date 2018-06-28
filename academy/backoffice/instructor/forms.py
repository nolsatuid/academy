from django import forms
from django.urls import reverse_lazy

from academy.apps.accounts.models import User, Profile, Instructor
from academy.core.fields import AjaxModelChoiceField
from academy.core.widget import ImagePreviewFileInput


class BaseInstructorForm(forms.Form):
    first_name = forms.CharField(label='Nama Awal')
    last_name = forms.CharField(label='Nama Akhir')
    linked_in = forms.URLField(label='LinkedIn')
    specialization = forms.CharField(label='Spesialisasi')
    avatar = forms.ImageField(label='Avatar', widget=ImagePreviewFileInput, required=False)

    def save(self, user=None):
        if user:
            first_name = self.cleaned_data['first_name']
            last_name = self.cleaned_data['last_name']
            linked_in = self.cleaned_data['linked_in']
            specialization = self.cleaned_data['specialization']
            avatar = self.cleaned_data['avatar']

            user.role = User.ROLE.trainer
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if hasattr(user, 'profile'):
                user.profile.specialization = specialization
                if avatar:
                    user.profile.avatar = avatar
                user.profile.linkedin = linked_in
                user.profile.save()
            else:
                profile = Profile(specialization=specialization, avatar=avatar, linkedin=linked_in, user=user)
                profile.save()

            if not hasattr(user, 'instructor'):
                instructor = Instructor(user=user)
                instructor.save()


class AddInstructorForm(BaseInstructorForm):
    user = AjaxModelChoiceField(model=User,
                                url=reverse_lazy('backoffice:instructors:ajax_find_user'),
                                label='Instruktur',
                                placeholder="Pilih User")

    field_order = ['user']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['avatar'] and not cleaned_data['user'].profile.avatar:
            self.add_error('avatar', 'Bidang ini tidak boleh kosong.')
        return cleaned_data

    def save(self, *args, **kwargs):
        user = self.cleaned_data['user']

        super().save(user=user)


class EditInstructorForm(BaseInstructorForm):
    user = forms.CharField(disabled=True)
    field_order = ['user']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['avatar']:
            self.add_error('avatar', 'Bidang ini tidak boleh kosong.')
        return cleaned_data

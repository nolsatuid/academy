from django import forms
from django.forms.formsets import BaseFormSet

from academy.apps.accounts.models import User
from academy.apps.students.models import TrainingMaterial, Training, Student, TrainingStatus
from model_utils import Choices


class TrainingMaterialForm(forms.ModelForm):

    class Meta:
        model = TrainingMaterial
        fields = {'code', 'title'}
        labels = {
            'code': 'Kode Materi',
            'title': 'Judul Materi'
        }


class StudentFilterForm(forms.Form):

    STATUS = Choices (
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
        (4, 'graduate', 'Lulus'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")
    batch = forms.ModelChoiceField(
        queryset=Training.objects.order_by('batch'), empty_label="Pilih Angkatan", required=False
    )
    training_materials = forms.ModelChoiceField( empty_label="Pilih Materi",
        queryset=TrainingMaterial.objects.all()
    )

    def clean(self):
        cleaned_data = super().clean()
        training_materials = cleaned_data['training_materials']
        training = cleaned_data['batch']
        if not training.materials.filter(id=training_materials.id).exists():
            raise forms.ValidationError(f"{training} tidak memiliki materi {training_materials}")

        return cleaned_data

    def get_data(self):
        status = self.cleaned_data['status']
        training_materials = self.cleaned_data['training_materials']
        batch = self.cleaned_data['batch']

        return Student.objects.filter(status=status, training=batch)\
            .select_related('training', 'user')


class ChangeStatusTraining(forms.ModelForm):
    STATUS = Choices(
        (1, 'not_yet', 'Belum'),
        (2, 'graduate', 'Lulus'),
        (3, 'repeat', 'Ulang'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="")

    class Meta:
        model = TrainingStatus
        fields = ('user', 'status')
        widgets = {
            'user': forms.Select(attrs={'hidden': True}),
        }


class BaseStatusTrainingFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        """
        To create dynamic label form fields training materials
        """
        self.students = kwargs.pop('students')
        super().__init__(*args, **kwargs)
        for i, form in enumerate(self.forms):
            # skip or continue last loop
            if i > self.students.count() - 1:
                continue
            user = self.students[i].user
            form.fields['user'].label = f"{user.username} - {user.name}"

    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            cleaned_data = form.cleaned_data
            print(cleaned_data)

    def save(self, training_material):
        for form in self.forms:
            cleaned_data = form.cleaned_data
            if cleaned_data:
                user = cleaned_data['user']
                status = cleaned_data['status']
                training_status = TrainingStatus.objects \
                    .filter(training_material=training_material, user=user).first()

                # to update or create
                if not training_status:
                    training_status = form.save(commit=False)
                else:
                    training_status.user = user
                    training_status.status = int(status)

                training_status.training_material = training_material
                training_status.save()


class BulkStatusTrainingForm(forms.Form):
    STATUS = Choices(
        (1, 'not_yet', 'Belum'),
        (2, 'graduate', 'Lulus'),
        (3, 'repeat', 'Ulang'),
    )
    status = forms.ChoiceField(choices=STATUS)

    def __init__(self, student_ids=None, *args, **kwargs):
        self.users = None
        self.student_ids = student_ids
        self.training_material = kwargs.pop('training_material')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if not self.student_ids:
            raise forms.ValidationError("Harus memilih minimal 1 pengguna", code="no_users")
        self.users = User.objects.filter(students__in=self.student_ids)
        return cleaned_data

    def save(self, *args, **kwargs):
        cleaned_data = super().clean()
        status_trainings = TrainingStatus.objects.filter(
            user__in=self.users, training_material=self.training_material)

        status_trainings.update(status=cleaned_data['status'])

    def send_notification(self):
        students = Student.objects.filter(id__in=self.student_ids)

        for student in students:
            training_materials = student.training.materials.prefetch_related('training_status')
            student.user.notification_status_training(training_materials)

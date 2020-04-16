import csv

from io import StringIO
from datetime import timedelta

from django.db.models import Q
from django import forms
from django.utils import timezone
from django.forms.formsets import BaseFormSet

from academy.apps.accounts.models import User
from academy.apps.students.models import Student, TrainingStatus, Training
from academy.core.utils import normalize_datetime_range
from academy.core.templatetags.form_tags import get_status_student, status_to_display
from model_utils import Choices


class BaseFilterForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Cari: nama/username'}),
        required=False
    )
    start_date = forms.DateField(
        input_formats=["%Y-%m-%d"], label="Tanggal Mulai", required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tanggal Mulai'}),
    )
    end_date = forms.DateField(
        input_formats=["%Y-%m-%d"], label="Tanggal Akhir", required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tanggal Akhir'}),
    )
    STATUS = Choices(
        ('', 'none', '-- Pilih --'),
        (1, 'selection', 'Seleksi'),
        (5, 'pre_test', 'Pre-Test'),
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
        (4, 'graduate', 'Lulus'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")
    batch = forms.ModelChoiceField(
        queryset=Training.objects.order_by('batch'), empty_label="Pilih Angkatan", required=False
    )

    def __init__(self, *args, **kwargs):
        self.users = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']

        if not start_date or not end_date:
            return cleaned_data

        if cleaned_data['start_date'] > cleaned_data['end_date']:
            self.add_error('start_date', "Tanggal mulai tidak bisa lebih dari tanggal akhir")

        today = timezone.now().date()

        if start_date > today:
            self.add_error('start_date', "Tanggal mulai tidak boleh lebih hari ini")

        if end_date > today:
            self.add_error('end_date', "Tanggal Akhir tidak boleh lebih dari hari ini")

        return cleaned_data

    def get_data(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        status = self.cleaned_data['status']
        name = self.cleaned_data['name']
        batch = self.cleaned_data['batch']

        students = Student.objects.exclude(user__username='deleted')
        if status:
            students = students.filter(status=status)

        if batch:
            students = students.filter(training=batch)

        user_ids = students.distinct('user_id') \
            .values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids).exclude(is_superuser=True).exclude(is_staff=True)

        if start_date and end_date:
            start, end = normalize_datetime_range(start_date, end_date)
            users = users.filter(date_joined__range=(start, end))

        if name:
            users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name) |
                                 Q(username__icontains=name))

        self.users = users
        return self.users

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'ID', 'Name', 'Username', 'Email', 'No. Ponsel', 'Status'
        ])

        for index, user in enumerate(self.users, 1):
            writer.writerow([
                index, user.id, user.name, user.username, user.email, user.phone,
                status_to_display(get_status_student(user))
            ])
        return csv_buffer


class ParticipantsFilterForm(BaseFilterForm):
    STATUS = Choices(
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")


class ChangeStatusTraining(forms.ModelForm):
    STATUS = Choices(
        (1, 'not_yet', 'Belum'),
        (2, 'graduate', 'Lulus'),
        (3, 'repeat', 'Ulang'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="")

    class Meta:
        model = TrainingStatus
        exclude = ('user',)
        widgets = {
            'training_material': forms.Select(attrs={'hidden': True}),
        }


class BaseStatusTrainingFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        """
        To create dynamic label form fields training materials
        """
        self.training_materials = kwargs.pop('training_materials')
        super().__init__(*args, **kwargs)
        for i, form in enumerate(self.forms):
            # skip or continue last loop
            if i > len(self.training_materials) - 1:
                continue
            material = self.training_materials[i]
            if material:
                form.fields['training_material'].label = f"{material.code} - {material.title}"

    def clean(self):
        if any(self.errors):
            return

    def save(self, user):
        for form in self.forms:
            cleaned_data = form.cleaned_data
            if cleaned_data:
                training_material = cleaned_data.get('training_material')
                status = cleaned_data.get('status')

                training_status = TrainingStatus.objects \
                    .filter(training_material=training_material, user=user).first()

                # to update or create
                if not training_status:
                    training_status = form.save(commit=False)
                else:
                    training_status.training_material = training_material
                    training_status.status = int(status)

                training_status.user = user
                training_status.save()


class DateInput(forms.DateInput):
    input_type = 'date'


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('batch', 'materials', 'link_group', 'start_date', 'end_date')
        labels = {
            'batch': 'Angkatan',
            'materials': 'Materi Pelatihan',
            'link_group': 'Link Grup Telegram',
            'start_date': 'Tanggal Mulai',
            'end_date': 'Tanggal Akhir'
        }
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
        help_texts = {
            'start_date': 'Boleh kosong',
            'end_date': 'Boleh kosong',
            'link_group': 'Boleh kosong',
            'materials': '',
            'batch': 'Gunakan awalan NSC- jika akan membuat angkatan baru untuk NolSatu Kampus, mis. NSC-1'
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('training',)
        labels = {
            'training': 'Peserta Angkatan'
        }


class ChangeStatusForm(forms.ModelForm):
    STATUS = Choices(
        (1, 'selection', 'Seleksi'),
        (5, 'pre_test', 'Pre-Test'),
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang')
    )
    status = forms.ChoiceField(choices=STATUS)

    class Meta:
        model = Student
        fields = ('status',)


class ChangeToParticipantForm(forms.Form):
    training = forms.ModelChoiceField(queryset=Training.objects.order_by('batch'), label="Angkatan")

    def save(self, student):
        student.status = Student.STATUS.participants
        student.training = self.cleaned_data['training']
        student.save()
        student.notification_status()


class LastLoginForm(forms.Form):
    start_date_time = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"], label="Tanggal Mulai", required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tanggal Mulai'}),
    )
    end_date_time = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"], label="Tanggal Akhir", required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tanggal Akhir'}),
    )

    def __init__(self, *args, **kwargs):
        self.users = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        start_date_time = cleaned_data['start_date_time']
        end_date_time = cleaned_data['end_date_time']

        if not start_date_time or not end_date_time:
            return cleaned_data

        if start_date_time > end_date_time:
            self.add_error('start_date_time', "Tanggal mulai tidak bisa lebih dari tanggal akhir")

        today = timezone.now()

        if start_date_time > today:
            self.add_error('start_date_time', "Tanggal mulai tidak boleh lebih hari ini")

        if end_date_time > today:
            self.add_error('end_date_time', "Tanggal Akhir tidak boleh lebih dari hari ini")

        return cleaned_data

    def get_data(self):
        start_date_time = self.cleaned_data['start_date_time']
        end_date_time = self.cleaned_data['end_date_time']

        users = User.objects.exclude(is_superuser=True).exclude(is_staff=True)

        if start_date_time and end_date_time:
            start, end = normalize_datetime_range(start_date_time, end_date_time)
            users = users.filter(date_joined__range=(start, end))

        self.users = users
        return self.users

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'Name', 'Username', 'Email', 'Masuk Terakhir'
        ])

        for index, user in enumerate(self.users, 1):
            if user.last_login:
                last_login = user.last_login.strftime("%d-%m-%Y %H:%M:%S")
            else:
                last_login = "-"

            writer.writerow([
                index, user.name, user.username, user.email, last_login
            ])
        return csv_buffer

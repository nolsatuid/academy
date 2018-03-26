import csv

from io import StringIO
from datetime import timedelta

from django.db.models import Q
from django import forms
from django.utils import timezone

from academy.apps.accounts.models import User
from academy.apps.students.models import Student
from academy.core.utils import normalize_datetime_range
from academy.core.templatetags.form_tags import get_status_student, status_to_display
from model_utils import Choices


class BaseFilterForm(forms.Form):

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Cari berdasarkan nama'}),
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
    STATUS = Choices (
        (1, 'selection', 'Seleksi'),
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
        (4, 'graduate', 'Lulus')
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")

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

        user_ids = Student.objects.filter(status=status).distinct('user_id') \
            .values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids).exclude(is_superuser=True).exclude(is_staff=True)

        if start_date and end_date:
            start, end = normalize_datetime_range(start_date, end_date)
            users = users.filter(date_joined__range=(start, end))

        if name:
            users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        self.users = users
        return self.users

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'ID', 'Name', 'Email', 'No. Ponsel', 'Status'
        ])

        for user in self.users:
            writer.writerow([
                user.id, user.name, user.email, user.phone,
                status_to_display(get_status_student(user))
            ])
        return csv_buffer


class ParticipantsFilterForm(BaseFilterForm):
    STATUS = Choices (
        (2, 'participants', 'Peserta'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")

import csv

from io import StringIO

from django import forms
from django.db.models import Q
from model_utils import Choices

from academy.apps.surveys.model import Survey
from academy.core.templatetags.form_tags import get_status_student, status_to_display


class SurveyFilterForm(forms.Form):
    WORKING_STATUS_CHOICES = Choices(
        ('', '-- Status Pekerjaan --'),
        (1, 'employee', 'Karyawan'),
        (2, 'student', 'Mahasiswa'),
        (3, 'unemployed', 'Belum Bekerja'),
        (99, 'other', 'Lain-lain')
    )

    GRADUATE_CHANNELED_TIME_CHOICES = Choices(
        ('', '-- Waktu disalurkan --'),
        (1, 'soon', 'Segera'),
        (99, 'other', 'Lain-lain')
    )

    TRUE_FALSE_CHOICES = (
        ('', '-- Bersedia disalurkan --'),
        (True, 'Ya'),
        (False, 'Tidak')
    )

    STATUS = Choices(
        ('', 'none', '-- Status --'),
        (1, 'selection', 'Seleksi'),
        (5, 'pre_test', 'Pre-Test'),
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
        (4, 'graduate', 'Lulus'),
    )

    LOCATION = Choices(
        ('', '-- Lokasi penyaluran --'),
        ('Jakarta', 'Jakarta'),
        ('Yogyakarta', 'Yogyakarta'),
        ('Bandung', 'Bandung'),
        ('Lain-lain', 'Lain-lain'),
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Cari: nama/username'}),
        required=False
    )
    work_status = forms.ChoiceField(choices=WORKING_STATUS_CHOICES, required=False)
    channeled = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, required=False)
    channeled_when = forms.ChoiceField(choices=GRADUATE_CHANNELED_TIME_CHOICES, required=False)
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")
    channeled_location = forms.ChoiceField(label="Lokasi penempatan", choices=LOCATION, required=False)

    def get_data(self):
        name = self.cleaned_data['name']
        work_status = self.cleaned_data['work_status']
        channeled = self.cleaned_data['channeled']
        channeled_when = self.cleaned_data['channeled_when']
        status = self.cleaned_data['status']
        location = self.cleaned_data['channeled_location']

        surveys = Survey.objects.filter(user__students__isnull=False).all()

        if name:
            surveys = surveys.filter(Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name) |
                                 Q(user__username__icontains=name))

        if work_status:
            surveys = surveys.filter(working_status=work_status)

        if channeled:
            surveys = surveys.filter(graduate_channeled=channeled)

        if channeled_when:
            surveys = surveys.filter(graduate_channeled_when=channeled_when)

        if status:
            surveys = surveys.filter(user__students__status=status)

        if location:
            if location == 'Lain-lain':
                surveys = surveys.exclude(channeled_location_other=[])
            else:
                surveys = surveys.filter(channeled_location__contains=[location])

        self.surveys = surveys

        return surveys

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'ID', 'Nama', 'Status','Status Pekerjaan', 'Bersedia Disalurkan', 'Waktu Disalurkan'
        ])

        for survey in self.surveys:
            writer.writerow([
                survey.id, survey.user.name,
                status_to_display(get_status_student(survey.user)),
                survey.get_working_status_display() if survey.working_status != 99 else survey.working_status_other,
                'Ya' if survey.graduate_channeled else 'Tidak',
                survey.get_graduate_channeled_when_display() if survey.graduate_channeled_when != 99 else survey.graduate_channeled_when_other
            ])
        return csv_buffer

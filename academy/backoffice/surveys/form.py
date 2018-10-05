import csv

from io import StringIO

from django import forms
from model_utils import Choices

from academy.apps.surveys.model import Survey


class SurveyFilterForm(forms.Form):
    WORKING_STATUS_CHOICES = Choices(
        ('', 'Status Pekerjaan'),
        (1, 'employee', 'Karyawan'),
        (2, 'student', 'Mahasiswa'),
        (3, 'unemployed', 'Belum Bekerja'),
        (99, 'other', 'Lain-lain')
    )

    GRADUATE_CHANNELED_TIME_CHOICES = Choices(
        ('', 'Waktu disalurkan'),
        (1, 'soon', 'Segera'),
        (99, 'other', 'Lain-lain')
    )

    TRUE_FALSE_CHOICES = (
        ('', 'Bersedia disalurkan'),
        (True, 'Ya'),
        (False, 'Tidak')
    )

    work_status = forms.ChoiceField(choices=WORKING_STATUS_CHOICES, required=False)
    channeled = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, required=False)
    channeled_when = forms.ChoiceField(choices=GRADUATE_CHANNELED_TIME_CHOICES, required=False)

    def get_data(self):
        work_status = self.cleaned_data['work_status']
        channeled = self.cleaned_data['channeled']
        channeled_when = self.cleaned_data['channeled_when']

        surveys = Survey.objects.all()
        if work_status:
            surveys = surveys.filter(working_status=work_status)

        if channeled:
            surveys = surveys.filter(graduate_channeled=channeled)

        if channeled_when:
            surveys = surveys.filter(graduate_channeled_when=channeled_when)

        self.surveys = surveys

        return surveys

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'ID', 'Name', 'Status Pekerjaan', 'Bersedia Disalurkan', 'Waktu Disalurkan'
        ])

        for survey in self.surveys:
            writer.writerow([
                survey.id, survey.user.name,
                survey.get_working_status_display() if survey.working_status != 99 else survey.working_status_other,
                'Ya' if survey.graduate_channeled else 'Tidak',
                survey.get_graduate_channeled_when_display() if survey.graduate_channeled_when != 99 else survey.graduate_channeled_when_other
            ])
        return csv_buffer

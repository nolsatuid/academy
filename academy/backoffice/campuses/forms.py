import csv

from io import StringIO

from django import forms
from django.db.models import Q

from academy.apps.campuses.models import Campus
from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training
from academy.core.templatetags.form_tags import get_status_student, status_to_display
from model_utils import Choices


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ['name', 'logo', 'description', 'address', 'email', 'phone', 'open_registration']


class BaseFilterForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Cari: nama/username'}),
        required=False
    )
    STATUS = Choices(
        ('', 'none', '-- Pilih --'),
        (1, 'selection', 'Seleksi'),
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
        (4, 'graduate', 'Lulus'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")
    batch = forms.ModelChoiceField(
        queryset=Training.objects.filter(batch__contains="NSC").order_by('batch'), empty_label="Pilih Angkatan", required=False
    )
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.all(), empty_label="Pilih Kampus", required=False
    )

    def __init__(self, *args, **kwargs):
        self.users = None
        super().__init__(*args, **kwargs)

    def get_data(self):
        status = self.cleaned_data['status']
        name = self.cleaned_data['name']
        batch = self.cleaned_data['batch']
        campus = self.cleaned_data['campus']

        students = Student.objects.filter(campus__isnull=False).exclude(user__username='deleted')
        if status:
            students = students.filter(status=status)

        if batch:
            students = students.filter(training=batch)

        if campus:
            students = students.filter(campus=campus)

        user_ids = students.distinct('user_id') \
            .values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids).exclude(is_superuser=True).exclude(is_staff=True)

        if name:
            users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name) |
                                 Q(username__icontains=name))

        self.users = users
        return self.users

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'ID', 'Name', 'Username', 'Email', 'No. Ponsel', 'Kampus', 'Status'
        ])
        for index, user in enumerate(self.users, 1):
            writer.writerow([
                index, user.id, user.name, user.username, user.email, user.phone, user.get_student().campus,
                status_to_display(get_status_student(user))
            ])

        return csv_buffer


class ParticipantsFilterForm(BaseFilterForm):
    STATUS = Choices(
        (2, 'participants', 'Peserta'),
        (3, 'repeat', 'Mengulang'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="Status")
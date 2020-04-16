import csv
from io import StringIO

from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from academy.apps.accounts.models import User, Profile
from academy.apps.offices.models import Setting
from academy.apps.students.models import Student, Training
from academy.core import validators

CSV_COLUMNS = ['nama depan', 'nama belakang', 'email', 'alamat']


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = ('name',)


class ImportUserForm(forms.Form):
    csv_file = forms.FileField(
        help_text=f"Format kolom yang didikung `{', '.join(CSV_COLUMNS)}`",
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
    )
    super_user = forms.BooleanField(
        help_text="Buat akun sebagai super admin", required=False,
        initial=False
    )
    status = forms.ChoiceField(
        choices=User.ROLE
    )

    def __init__(self, *args, **kwargs):
        self.reject_data = []
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        read_file = self.read_file()
        if len(next(read_file)) != len(CSV_COLUMNS):
            raise forms.ValidationError("Jumlah kolom tidak sesuai")
        return cleaned_data

    def read_file(self):
        csvfile = self.cleaned_data['csv_file']
        csvfile.seek(0)
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            yield row

    def validate_email(self, email):
        try:
            validators.validate_email_address(email)
            return True
        except ValidationError:
            return False

    def create_user(self, row):
        username = row[2].split('@')[0]
        user = User.objects.create_user(
            username=username, email=row[2], password="academy!@#",
            registered_via=User.VIA.import_file, role=User.ROLE.student,
            first_name=row[0], last_name=row[1], is_superuser=self.cleaned_data['super_user'],
            is_staff=self.cleaned_data['super_user']
        )
        user.is_active = True
        user.save()

        Profile.objects.create(user=user, address=row[3])
        training = Training.get_or_create_initial()
        Student.objects.create(user=user, training=training)

    def import_data(self):
        data = self.read_file()
        for row in data:
            email = row[2].strip("")
            if self.validate_email(email) and \
                    not User.objects.filter(email=email).exists():
                self.create_user(row)
                continue
            self.reject_data.append(row)

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        for row in self.reject_data:
            writer.writerow([
                row[0], row[1], row[2], row[3]
            ])
        return csv_buffer
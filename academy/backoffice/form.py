import csv
from io import StringIO

from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

from academy.apps.accounts.models import User, Profile
from academy.apps.offices.models import Setting, AuthSetting
from academy.apps.students.models import Student, Training
from academy.core import validators

CSV_COLUMNS = [
    'nama depan', 'nama belakang', 'email', 'alamat',
    'username', 'password'
]


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        exclude = ('name',)


class AuthSettingForm(forms.ModelForm):
    class Meta:
        model = AuthSetting
        fields = ('sign_with_btech',)


class ImportUserForm(forms.Form):
    csv_file = forms.FileField(
        help_text=f"Format kolom yang didikung `{', '.join(CSV_COLUMNS)}`",
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
    )
    status = forms.ChoiceField(
        choices=User.ROLE
    )
    super_user = forms.BooleanField(
        help_text="Buat akun sebagai super admin", required=False,
        initial=False
    )
    generate_username = forms.BooleanField(
        help_text="Otomatis membuat username", required=False,
        initial=False
    )
    default_password = forms.BooleanField(
        help_text="Gunakan default password adalah academy!@#", required=False,
        initial=True
    )
    update_or_create = forms.BooleanField(
        label='Akti Update` atau `Create`',
        help_text="Jika ya, maka aksi akan diubah menjadi update",
        required=False, initial=False
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
        user = User.objects.create_user(
            username=self.get_username(row), email=row[2],
            password=self.get_password(row), registered_via=User.VIA.import_file,
            role=User.ROLE.student, first_name=row[0], last_name=row[1],
            is_superuser=self.cleaned_data['super_user'],
            is_staff=self.cleaned_data['super_user']
        )
        user.is_active = True
        user.save()

        Profile.objects.create(user=user, address=row[3])
        training = Training.get_or_create_initial()
        Student.objects.create(user=user, training=training)

    def update_user(self, row):
        user = User.objects.filter(email=row[2]).first()
        if user:
            user.username = self.get_username(row)
            user.set_password(self.get_password(row))
            user.role = User.ROLE.student
            user.first_name = row[0]
            user.last_name = row[1]
            user.is_superuser = self.cleaned_data['super_user']
            user.is_staff = self.cleaned_data['super_user']
            user.save()

    def import_data(self):
        data = self.read_file()

        if self.cleaned_data['update_or_create']:
            for row in data:
                email = row[2].strip("")
                username = row[4].strip("")
                if self.validate_email(email) and \
                        User.objects.filter(Q(email=email) | Q(username=username)).exists():
                    self.update_user(row)
                    continue
                self.reject_data.append(row)
        else:
            for row in data:
                email = row[2].strip("")
                username = row[4].strip("")
                if self.validate_email(email) and \
                        not User.objects.filter(Q(email=email) | Q(username=username)).exists():
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

    def get_username(self, row):
        if self.cleaned_data['generate_username']:
            username = row[2].split('@')[0]
        else:
            username = row[4].strip()
        return username

    def get_password(self, row):
        if self.cleaned_data['default_password']:
            password = "academy!@#"
        else:
            password = row[5].strip()
        return password

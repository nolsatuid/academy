from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from model_utils import Choices

from academy.apps.accounts.models import User, Profile
from academy.apps.students.models import Student
from academy.apps.surveys.model import Survey
from academy.core import fields
from academy.core.validators import validate_email, validate_mobile_phone, validate_username

from post_office import mail


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Email atau Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Kata Sandi'})


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].validators = [validate_username]

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.is_active = False
        user.role = User.ROLE.student
        user.save()
        user.notification_register()

        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=70, label='Nama Depan')
    last_name = forms.CharField(max_length=70, required=False, label='Nama Belakang')
    phone_number = forms.CharField(max_length=16, validators=[validate_mobile_phone],
                                   label='Nomor Ponsel')
    curriculum_vitae = fields.FileFieldExtended(
        label=mark_safe('Curriculum Vitae<br/>'
                        '<a href="https://www.dropbox.com/s/nqjoadgifz7zpb0/template_cv_nolsatu.docx?dl=0" target="_blank">'
                        'Download Template CV</a>'),
        help_text="File Type: .doc, .docx. Max 2 MB. Mohon gunakan template yang disediakan",
        max_mb_file_size=2,
        allowed_content_type=[
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ]
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'linkedin', 'git_repo',
                  'blog', 'youtube', 'facebook', 'instagram', 'twitter', 'telegram_id', 'curriculum_vitae')
        help_texts = {
            'git_repo': ('url akun github/gitlab/bitbucket dll'),
            'blog': ('url blog atau portfolio'),
            'youtube': ('url kanal youtube'),
            'facebook': ('contoh: "https://www.facebook.com/namaanda"'),
            'linkedin': ('contoh: "https://www.linkedin.com/in/namaanda/"'),
            'instagram': ('username Instagram'),
            'twitter': ('username Twitter tanpa "@"'),
            'telegram_id': ('contoh "@namaanda"'),
        }

    def __init__(self, cv_required=True, *args, **kwargs):
        # cv_required is argument to create optional this form required cv or not
        # by default cv_required is True
        self.cv_required = cv_required
        super().__init__(*args, **kwargs)
        self.fields['curriculum_vitae'].required = self.cv_required

    def clean_telegram_id(self):
        telegram_id = self.cleaned_data['telegram_id']
        if not telegram_id:
            return telegram_id

        if telegram_id[0] != '@':
            raise forms.ValidationError("Awal ID harus menggunakan karakter '@'")
        return telegram_id

    def save(self, user, *args, **kwargs):
        profile = super().save(commit=False)
        profile.user = user
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.phone = self.cleaned_data['phone_number']
        profile.user.save()
        profile.save()

        return profile


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('user', 'training', 'campus')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(validators=[validate_email], label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Email anda'}),
                             help_text='Kami akan mengirim email untuk mengatur ulang kata sandi Anda')

    # The link to reset your password will be sent to your email
    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError("Email tidak terdaftar")

        return user

    def send_email(self, user):
        data = {
            'token': default_token_generator.make_token(user),
            'uid': int_to_base36(user.id),
            'host': settings.HOST,
            'user': user,
            'email_title': 'Lupa kata sandi'
        }

        mail.send(
            [user.email],
            settings.DEFAULT_FROM_EMAIL,
            subject='Lupa Kata Sandi',
            context=data,
            html_message=render_to_string('emails/forgot_password.html', context=data)
        )


class SurveyForm(forms.ModelForm):
    LOCATION = Choices(
        ('Jakarta', 'Jakarta'),
        ('Yogyakarta', 'Yogyakarta'),
        ('Bandung', 'Bandung'),
        ('Lain-lain', 'Lain-lain'),
    )

    working_status = forms.ChoiceField(choices=Survey.WORKING_STATUS_CHOICES, label='Status pekerjaan saat ini:',
                                       widget=forms.RadioSelect)
    working_status_other = forms.CharField(label='Jawaban anda:', required=False)
    graduate_channeled = forms.ChoiceField(choices=Survey.TRUE_FALSE_CHOICES,
                                           label='Apabila Anda telah lulus dari kelas nolsatu, apakah bersedia untuk disalurkan',
                                           widget=forms.RadioSelect)
    graduate_channeled_when = forms.ChoiceField(choices=Survey.GRADUATE_CHANNELED_TIME_CHOICES,
                                                label='Apabila bersedia untuk disalurkan, kapan waktu yang diinginkan',
                                                widget=forms.RadioSelect)
    graduate_channeled_when_other = forms.CharField(label='Jawaban anda:', required=False)
    channeled_location = forms.MultipleChoiceField(
        label="Apabila bersedia untuk disalurkan, dimana lokasi yang diinginkan",
        choices=LOCATION,
        widget=forms.CheckboxSelectMultiple, required=False)
    channeled_location_other = forms.CharField(label='Jawaban anda (Pisahkan dengan koma):', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Because [] also mean false so check it against None
        if self.initial.get('channeled_location_other', None) is not None:
            self.initial['channeled_location_other'] = ','.join(self.initial['channeled_location_other'])

    def clean_channeled_location_other(self):
        return self.cleaned_data['channeled_location_other'].split(',')

    def clean(self):
        if 'Lain-lain' not in self.cleaned_data['channeled_location']:
            self.cleaned_data['channeled_location_other'] = []

    class Meta:
        model = Survey
        exclude = ['user']

    def save(self, user, *args, **kwargs):
        survey = super().save(commit=False)
        if not hasattr(survey, 'user'):
            survey.user = user

        survey.save()

        return survey


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

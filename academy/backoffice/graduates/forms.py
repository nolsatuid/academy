import csv

from io import StringIO

from django.db.models import Q
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.urls import reverse

from academy.backoffice.users.forms import BaseStatusTrainingFormSet
from academy.apps.students.models import Student, Training, TrainingStatus, TrainingMaterial
from academy.apps.accounts.models import User, Inbox
from academy.core.fields import TrainingMaterialField
from academy.apps.graduates.models import Graduate

from post_office import mail
from model_utils import Choices


class ParticipantsRepeatForm(forms.Form):
    batch = forms.ModelChoiceField(
        label='Angkatan', queryset=Training.objects.order_by('batch'), empty_label="Pilih Angkatan",
        help_text="Pemberitahuan akan dikirim kesemua peserta tidak " \
        "lulus pada angkatan yang dipilih"
    )

    def __init__(self, *args, **kwargs):
        self.users_repeat = []
        super().__init__(*args, **kwargs)

    def clean(self):
        batch = self.cleaned_data['batch']
        students = Student.objects.filter(status=Student.STATUS.participants, training=batch)
        if not students:
            raise forms.ValidationError("Maaf tidak ada peserta pada angkatan ini")

        user_ids = students.values_list("user_id", flat=True)
        users = User.objects.filter(id__in=user_ids)

        for user in users:
            status = user.get_count_training_status()
            if status['graduate'] < settings.INDICATOR_GRADUATED and status['not_yet'] == 0 \
                    and status['repeat'] >= settings.INDICATOR_REPEATED:
                self.users_repeat.append({'user': user, 'status': status})

        if not self.users_repeat:
            raise forms.ValidationError("Tidak ada peserta yang mengulang")

        return batch

    def send_notification(self):
        title = "Maaf, Anda belum bisa lanjut"

        context = {
            'host': settings.HOST,
            'email_title': title,
            'indicator': settings.INDICATOR_GRADUATED
        }

        for data in self.users_repeat:
            context['user'] = data['user']
            context['graduate'] = data['status']['graduate']
            html_message=render_to_string('emails/participants_repeat.html', context=context)

            Inbox.objects.create(user=data['user'], subject=title, content=html_message)

            mail.send(
                data['user'].email,
                settings.DEFAULT_FROM_EMAIL,
                subject=title,
                html_message=html_message
            )
            student = data['user'].get_student()
            student.status = Student.STATUS.repeat
            student.save(update_fields=['status'])

        return len(self.users_repeat)


class AddTrainingStatus(forms.ModelForm):
    training_material = TrainingMaterialField()
    STATUS = Choices(
        (1, 'not_yet', 'Belum'),
        (2, 'graduate', 'Lulus'),
        (3, 'repeat', 'Ulang'),
    )
    status = forms.ChoiceField(choices=STATUS, required=False, label="")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = TrainingStatus
        fields = ('training_material', 'status')

    def clean(self):
        cleaned_data = super().clean()
        if TrainingStatus.objects.filter(user=self.user, training_material=cleaned_data['training_material']).exists():
            raise forms.ValidationError(
                f"{self.user.name} sudah memiliki materi {cleaned_data['training_material']}"
            )
        return cleaned_data

    def save(self, *args, **kwargs):
        training_status = super().save(commit=False)
        training_status.user = self.user
        training_status.save()
        return training_status


class GraduateTrainingStatusFormSet(BaseStatusTrainingFormSet):

    def __init__(self, graduate, *args, **kwargs):
        """
        create label any button to action delete training status
        training material data get form user, not from batch
        """
        self.graduate = graduate
        self.user = graduate.user
        self.trainig = {
            'materials': [],
            'status': []
        }
        for ts in self.user.training_status.all():
            if ts.training_material:
                self.trainig['status'].append(ts)
                self.trainig['materials'].append(ts.training_material)

        super().__init__(training_materials=self.trainig['materials'], *args, **kwargs)
        for i, form in enumerate(self.forms):
            # skip or continue last loop
            if i > len(self.training_materials) - 1:
                continue
            material = self.trainig['materials'][i]
            status = self.trainig['status'][i]

            # create button to combine with label
            url = reverse('backoffice:graduates:delete_training_status', args=[status.id, graduate.id])
            html_button = '<a href="#" class="btn btn-primary btn-pill btn-sm" data-toggle="modal" data-target="#confirmDeleteModal"' \
                f'data-url="{url}" data-title="{material.title}" ><i class="fa fa-trash"></i></a>'
            label = mark_safe(f"{html_button} {material.code} - {material.title}")

            form.fields['training_material'].label = label


class BaseFilterForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Cari: nama/username'}),
        required=False
    )
    batch = forms.ModelChoiceField(
        queryset=Training.objects.order_by('batch'), empty_label="Pilih Angkatan", required=False
    )
    STATUS = (
        (None, 'Pilih Status'),
        (True, 'Tersalurkan'),
        (False, 'Belum Tersalurkan'),
    )
    is_channeled = forms.ChoiceField(label='Tersalurkan', required=False, choices=STATUS)

    def __init__(self, *args, **kwargs):
        self.graduates = None
        super().__init__(*args, **kwargs)

    def get_data(self):
        name = self.cleaned_data['name']
        batch = self.cleaned_data['batch']
        is_channeled = self.cleaned_data['is_channeled']
        graduates = Graduate.objects.select_related('user')

        if batch:
            graduates = graduates.filter(student__training=batch)
        if is_channeled:
            graduates = graduates.filter(is_channeled=is_channeled)
        if name:
            graduates = graduates.filter(
                Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name) |
                Q(user__username__icontains=name)
            )

        self.graduates = graduates
        return self.graduates

    def generate_to_csv(self):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow([
            'No.', 'Nama', 'No.Sertifikat', 'Email', 'No. Ponsel', 'Tersalurkan'
        ])
        for index, graduate in enumerate(self.graduates, 1):
            writer.writerow([
                index, graduate.user.name, graduate.certificate_number,
                graduate.user.email, graduate.user.phone,
                'Ya' if graduate.is_channeled else 'Tidak'
            ])

        return csv_buffer


class GraduateHasChanneledForm(forms.Form):
    channeled_at = forms.CharField(label='Tersalurkan pada', max_length=150, help_text='Nama Perusahaan')
    graduate_id = forms.CharField(max_length=100, label='', widget=forms.HiddenInput())

    def save(self):
        cleaned_data = super().clean()
        graduate = Graduate.objects.get(id=cleaned_data['graduate_id'])
        graduate.channeled_at = cleaned_data['channeled_at']
        graduate.is_channeled = True
        graduate.save()

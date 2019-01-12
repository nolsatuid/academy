from django import forms
from django.conf import settings
from django.template.loader import render_to_string

from academy.apps.students.models import Student, Training, TrainingStatus
from academy.apps.accounts.models import User
from post_office import mail


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

            mail.send(
                data['user'].email,
                settings.DEFAULT_FROM_EMAIL,
                subject=title,
                html_message=render_to_string('emails/participants_repeat.html', context=context)
            )
            student = data['user'].get_student()
            student.status = Student.STATUS.repeat
            student.save(update_fields=['status'])

        return len(self.users_repeat)


class AddTrainingStatus(forms.ModelForm):

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

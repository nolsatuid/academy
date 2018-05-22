from django import forms

from academy.apps.students.models import TrainingMaterial


class TrainingMaterialForm(forms.ModelForm):

    class Meta:
        model = TrainingMaterial
        fields = {'code', 'title'}
        labels = {
            'code': 'Kode Materi',
            'title': 'Judul Materi'
        }

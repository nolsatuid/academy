from urllib.parse import urlencode

from tests import AcademyTestCase
from django.test import Client
from django.urls import reverse

from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training, TrainingStatus
from academy.backoffice.training_materials.forms import StudentFilterForm


class TrainingMaterialTest(AcademyTestCase):
    fixtures = ['accounts.json', 'students.json']

    def setUp(self):
        super().setUp()
        self.admin = User.objects.filter(is_superuser=True).first()
        self.admin.set_password('123qweasd')
        self.admin.save()
        self.client = Client()

    def test_bulk_material_status(self):
        self.client.login(username=self.admin.email, password='123qweasd')

        response = self.client.get(reverse('backoffice:training_materials:bulk_material_status'))
        self.assertEqual(response.status_code, 200)

        training = Training.objects.first()
        training_material = training.materials.first()
        students = training.students.filter(status=Student.STATUS.participants,
                                            training__materials__id=training_material.id)
        data = {
            'students': list(students.values_list('id', flat=True)),
            'training_materials': training_material.id,
            'status': TrainingStatus.STATUS.graduate,
            'student_status': StudentFilterForm.STUDENT_STATUS.participants,
            'batch': training.id
        }
        query_params = urlencode(data)
        url = f"{reverse('backoffice:training_materials:bulk_material_status')}?{query_params}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        for student in students:
            materi = student.training.materials.get(id=training_material.id)
            status = materi.get_training_status(student.user).status
            self.assertEqual(status, TrainingStatus.STATUS.graduate)

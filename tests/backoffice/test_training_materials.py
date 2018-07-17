from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from academy.apps.accounts.models import User
from academy.apps.students.models import Student, Training, TrainingStatus


class TrainingMaterialTest(TestCase):
    fixtures = ['accounts.json', 'students.json']

    def setUp(self):
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
            'training_materials': training_material,
            'status': TrainingStatus.STATUS.not_yet
        }

        query_params = f"?training_materials={training_material.id}&batch={training.batch}"\
            f"&status={Student.STATUS.participants}"
        response = self.client.post(reverse('backoffice:training_materials:bulk_material_status')
                                            + query_params, data=data)
        self.assertEqual(response.status_code, 200)

        for student in students:
            materi = student.training.materials.get(id=training_material.id)
            status = materi.get_training_status(student.user).status
            self.assertEqual(status, TrainingStatus.STATUS.not_yet)

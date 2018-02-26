from django.test import TestCase

from academy.apps.accounts.models import User
from academy.apps.students.models import Training, Student
from academy.website.accounts.forms import StudentForm


class AccountsTestForm(TestCase):

    def test_student_form(self):
        training = Training.objects.create(batch=1)
        user = User.objects.create_user(
            'username', 'user@gmail.com', '123qwead', is_active=True
        )
        self.assertEqual(user.email, 'user@gmail.com')

        data = {
            'user': user.id,
            'training': training.id
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        student = Student.objects.first()
        self.assertEqual(student.user, user)
        self.assertEqual(student.training, training)

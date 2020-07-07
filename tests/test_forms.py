from tests import AcademyTestCase

from academy.apps.accounts.models import User
from academy.apps.students.models import Training, Student
from academy.website.accounts.forms import StudentForm, SignupForm
from academy.apps.campuses.models import Campus


class AccountsTestForm(AcademyTestCase):

    def test_signup_form(self):
        data = {
            'username': 'irfanpule',
            'email': 'irfan.pule2@gmail.com',
            'password1': 'irfanjadipeserta01',
            'password2': 'irfanjadipeserta01'
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'irfanpule')
        self.assertEqual(user.email, 'irfan.pule2@gmail.com')
        self.assertEqual(user.role, User.ROLE.student)

        # test fail
        data = {
            'username': '',
            'email': 'irfan.pule2@gmail.com',
            'password1': 'irfanjadipeserta01',
            'password2': 'irfanjadipeserta01'
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

        data = {
            'username': 'irfanpule',
            'email': 'irfan.pule2@gmail.com',
            'password1': 'irfanjadipeserta01',
            'password2': 'passwordbeda'
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

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

        # create student use data campus
        campus = Campus.objects.create(name="Nolsatu University")
        training = Training.objects.create(batch="NSC-1")
        user = User.objects.create_user(
            'irfanpule', 'irfanpule@gmail.com', '123qwead', is_active=True
        )
        self.assertEqual(user.email, 'irfanpule@gmail.com')

        data = {
            'user': user.id,
            'training': training.id,
            'campus': campus.id
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())
        student = form.save()
        self.assertEqual(student.user, user)
        self.assertEqual(student.training, training)
        self.assertEqual(student.campus, campus)

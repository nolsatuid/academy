from django.test import TestCase

from academy.apps.accounts.models import User
from academy.apps.graduates.models import Graduate


class GraduateTest(TestCase):
    fixtures = ['accounts.json', 'students.json']

    def test_generate_certificate_number(self):
        user = User.objects.get(email='user1@gmail.com')
        graduate = Graduate.objects.create(user=user, student=user.get_student())
        self.assertIsNotNone(graduate.certificate_number)

        batch = str(graduate.student.training.batch)
        batch = "0" + batch if len(batch) == 1 else batch

        user_id = str(graduate.user_id)
        user_id = "0" + user_id if len(user_id) == 1 else batch

        date = graduate.created.strftime("YYYY-MMDD")
        certificate_number = f"NS-{batch}{user_id}-{date}"
        self.assertEqual(graduate.certificate_number, certificate_number)

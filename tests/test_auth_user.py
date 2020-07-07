from tests import AcademyTestCase
from django.urls import reverse

from academy.apps.accounts.models import User
from academy.apps.surveys.model import Survey

from academy.website.accounts.forms import SurveyForm


class AuthUserViewTest(AcademyTestCase):
    fixtures = ['accounts.json', 'students.json']

    def test_auth_user(self):
        user = User.objects.get(email='user2@gmail.com')
        url = user.generate_auth_url()
        response = self.client.get(url)

        # kalau belum punya survey harus redirect ke survey
        self.assertRedirects(response, '/accounts/survey/', status_code=302, target_status_code=200, fetch_redirect_response=True)

        # test untuk user yang sudah memiliki memiliki survey
        # create survey
        data = {
            'working_status': Survey.WORKING_STATUS_CHOICES.employee,
            'graduate_channeled': True,
            'graduate_channeled_when': Survey.GRADUATE_CHANNELED_TIME_CHOICES.soon
        }
        form = SurveyForm(data=data)
        form.save(user)

        user.refresh_from_db()
        url = user.generate_auth_url()
        response = self.client.get(url)

        # kalau sudah punya survey harus redirect ke survey edit
        self.assertRedirects(response, '/accounts/survey/edit/', status_code=302, target_status_code=200, fetch_redirect_response=True)

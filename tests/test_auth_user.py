from django.test import TestCase
from django.urls import reverse

from academy.apps.accounts.models import User
from academy.apps.surveys.model import Survey

from academy.website.accounts.forms import SurveyForm


class AuthUserTest(TestCase):
    fixtures = ['accounts.json', 'students.json']

    def test_edit_survey(self):
        user = User.objects.get(email='user2@gmail.com')
        url = user.generate_auth_url()
        response = self.client.get(url)
        if hasattr(user, 'survey'):
            print("Has Survey")
            self.assertRedirects(response, '/accounts/survey/edit/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        else:
            print("Not Yet")
            self.assertRedirects(response, '/accounts/survey/', status_code=302, target_status_code=200, fetch_redirect_response=True)
            self.create_survey(user)
            self.test_edit_survey()

    def create_survey(self, user):
        #create survey
        data = {
            'working_status': Survey.WORKING_STATUS_CHOICES.employee,
            'graduate_channeled': True,
            'graduate_channeled_when': Survey.GRADUATE_CHANNELED_TIME_CHOICES.soon
        }
        form = SurveyForm(data=data)
        self.assertTrue(form.is_valid())
        form.save(user)
from django.test import TestCase
from django.urls import reverse

from academy.apps.accounts.models import User


class AuthUserTest(TestCase):
    fixtures = ['accounts.json', 'students.json']

    def test_edit_survey(self):
        user = User.objects.get(email='user2@gmail.com')
        url = user.generate_auth_url()
        response = self.client.get(url)
        if hasattr(user, 'survey'):
            self.assertRedirects(response, '/accounts/survey/edit/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        else:
            self.assertRedirects(response, '/accounts/survey/', status_code=302, target_status_code=200, fetch_redirect_response=True)
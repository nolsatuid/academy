from django.test import TestCase
from django.test import Client

from academy.apps.accounts.models import User, Inbox
from academy.apps.offices.models import Setting, AuthSetting


class AccountsUserViewTest(TestCase):
    fixtures = ['accounts.json', 'students.json']

    def setUp(self):
        Setting.objects.create()
        AuthSetting.objects.create()

    def test_inbox(self):
        user = User.objects.get(email='user2@gmail.com')
        user.set_password('password123')
        user.save()

        login = self.client.login(username=user.username, password='password123')
        self.assertTrue(login)

        # normal url
        url = '/accounts/inbox/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # with parameter page
        url = '/accounts/inbox/?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # wrong value parameter
        url = '/accounts/inbox/?page=1%27'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

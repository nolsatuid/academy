from tests import AcademyTestCase

from academy.apps.accounts.models import User, Inbox


class AccountsUserViewTest(AcademyTestCase):
    fixtures = ['accounts.json', 'students.json']

    def setUp(self):
        super().setUp()
        self.user = User.objects.get(email='user2@gmail.com')
        self.user.set_password('password123')
        self.user.save()

    def test_inbox(self):
        login = self.client.login(username=self.user.username, password='password123')
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

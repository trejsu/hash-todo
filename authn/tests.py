from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogoutViewTest(TestCase):

    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'pass123')

    def test_logout_should_redirect_to_login_page(self):
        # given:
        username = 'test'
        password = 'pass123'
        self.client.login(username=username, password=password)

        # when:
        response = self.client.get(reverse('logout'))

        # then:
        self.assertRedirects(response, '/auth/login/')

    def test_logout_should_work(self):
        # given:
        username = 'test'
        password = 'pass123'
        self.client.login(username=username, password=password)

        # when:
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('todo:home'))

        # then:
        self.assertRedirects(response, '/auth/login/?next=/todo/')

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):

    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'pass123')

    def test_unauthenticated_user_should_be_redirected_to_login_page(self):
        # when:
        response = self.client.get(reverse('todo:home'))

        # then:
        self.assertRedirects(response, '/auth/login/?next=/todo/')

    def test_authenticated_user_should_stay_on_home_page(self):
        # given:
        username = 'test'
        password = 'pass123'
        self.client.login(username=username, password=password)

        # when:
        response = self.client.get(reverse('todo:home'))

        # then:
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Hi {username}!')

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task, STATUS


def create_task(text, user, status=STATUS.active):
    Task.objects.create(text=text, user=user, status=status)


def create_user(username='test', password='test', email='test@test'):
    return User.objects.create_user(username=username, password=password, email=email)


def create_test_tasks():
    test_user = create_user(username='test', password='test', email='test@test')
    other_user = create_user(username='other', password='other', email='other@other')
    create_task('todo1', test_user)
    create_task('todo2', test_user)
    create_task('todo3', test_user)
    create_task('todo4', other_user)
    create_task('todo5', other_user)
    create_task('todo6', test_user, status=STATUS.done)


class HomeViewTests(TestCase):

    def setUp(self):
        create_test_tasks()

    def test_unauthenticated_user_should_be_redirected_to_login_page(self):
        # when:
        response = self.client.get(reverse('todo:home'))

        # then:
        self.assertRedirects(response, '/auth/login/?next=/todo/')

    def test_authenticated_user_should_stay_on_home_page(self):
        # given:
        username = 'test'
        password = 'test'
        self.client.login(username=username, password=password)

        # when:
        response = self.client.get(reverse('todo:home'))

        # then:
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Hi {username}!')

    def test_should_display_list_with_tasks_owned_by_current_user(self):
        # given
        username = 'test'
        password = 'test'
        logged_in_user = User.objects.get(username=username)
        self.client.login(username=username, password=password)

        # when
        response = self.client.get(reverse('todo:home'))

        # then
        expected = Task.objects.filter(user=logged_in_user)
        object_list = response.context['object_list']
        self.assertQuerysetEqual(object_list, expected, ordered=False, transform=lambda x: x)

    def test_should_display_list_with_active_tasks_only_when_done_parameter_is_set_to_false(self):
        # given
        username = 'test'
        password = 'test'
        logged_in_user = User.objects.get(username=username)
        self.client.login(username=username, password=password)

        # when
        response = self.client.get('/todo/?done=false')

        # then
        expected = Task.objects.filter(user=logged_in_user, status=STATUS.active)
        object_list = response.context['object_list']
        self.assertQuerysetEqual(object_list, expected, ordered=False, transform=lambda x: x)


class TaskModelTests(TestCase):

    def test_new_task_should_have_active_status(self):
        # given
        text = 'New todo'
        user = create_user()

        # when
        t = Task.objects.create(text=text, user=user)

        # then
        self.assertEqual(t.status, STATUS.active)

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from todo.models import Task
from .serializers import TaskSerializer


def create_task(text, user):
    Task.objects.create(text=text, user=user)


def create_user(username, password, email):
    return User.objects.create_user(username=username, password=password, email=email)


def create_test_tasks():
    test_user = create_user('test', 'test', 'test@test')
    other_user = create_user('other', 'other', 'other@other')
    create_task('todo1', test_user)
    create_task('todo2', test_user)
    create_task('todo3', test_user)
    create_task('todo4', other_user)
    create_task('todo5', other_user)


class GetAllTasksTest(APITestCase):
    client = APIClient()

    def setUp(self):
        create_test_tasks()

    def test_should_return_tasks_owned_by_logged_in_user(self):
        # given
        logged_in_user = User.objects.get(username='test')
        self.client.login(username='test', password='test')

        # when
        response = self.client.get(
            reverse("get-all-tasks", kwargs={"version": "v1"})
        )

        # then
        expected = Task.objects.filter(user=logged_in_user)
        serialized = TaskSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, 200)


class GetTaskTest(APITestCase):
    client = APIClient()

    def setUp(self):
        create_test_tasks()

    def test_should_return_task_if_its_owned_by_logged_in_user(self):
        # given
        self.client.login(username='test', password='test')
        task_id = 2
        expected = TaskSerializer(Task.objects.get(pk=task_id))

        # when
        response = self.client.get(
            reverse("get-task", kwargs={"version": "v1", "pk": task_id})
        )

        # then
        self.assertEqual(response.data, expected.data)
        self.assertEqual(response.status_code, 200)

    def test_should_return_404_when_task_is_not_owned_by_current_user(self):
        # given
        self.client.login(username='test', password='test')
        task_id = 4

        # when
        response = self.client.get(
            reverse("get-task", kwargs={"version": "v1", "pk": task_id})
        )

        # then
        self.assertEqual(response.status_code, 404)

    def test_should_return_404_when_task_does_not_exist(self):
        # given
        self.client.login(username='test', password='test')
        task_id = 10

        # when
        response = self.client.get(
            reverse("get-task", kwargs={"version": "v1", "pk": task_id})
        )

        # then
        self.assertEqual(response.status_code, 404)

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from todo.models import Task, STATUS
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


class AllTasksTest(APITestCase):
    client = APIClient()

    def setUp(self):
        create_test_tasks()

    def test_should_return_tasks_owned_by_logged_in_user(self):
        # given
        logged_in_user = User.objects.get(username='test')
        self.client.login(username='test', password='test')

        # when
        response = self.client.get(
            reverse("api:all-tasks", kwargs={"version": "v1"})
        )

        # then
        expected = Task.objects.filter(user=logged_in_user)
        serialized = TaskSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, 200)

    def test_should_add_new_task(self):
        # given
        self.client.login(username='test', password='test')
        task_data = {'text': 'new todo'}

        # when
        response = self.client.post(
            path=reverse("api:all-tasks", kwargs={"version": "v1"}),
            data=task_data
        )

        # then
        self.assertEqual(response.status_code, 201)
        new_task = TaskSerializer(Task.objects.get(pk=response.data['id'])).data
        self.assertEqual(response.data, new_task)


class TaskTest(APITestCase):
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
            reverse("api:task", kwargs={"version": "v1", "pk": task_id})
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
            reverse("api:task", kwargs={"version": "v1", "pk": task_id})
        )

        # then
        self.assertEqual(response.status_code, 404)

    def test_should_return_404_when_task_does_not_exist(self):
        # given
        self.client.login(username='test', password='test')
        task_id = 10

        # when
        response = self.client.get(
            reverse("api:task", kwargs={"version": "v1", "pk": task_id})
        )

        # then
        self.assertEqual(response.status_code, 404)

    def test_should_update_task_using_put_method(self):
        # given
        self.client.login(username='test', password='test')
        id = 1
        task = Task.objects.get(pk=id)
        self.assertEqual(task.status, STATUS.active)
        task.status = STATUS.done
        put_data = TaskSerializer(task).data

        # when
        response = self.client.put(
            path=reverse("api:task", kwargs={"version": "v1", "pk": id}),
            data=put_data
        )
        updated_task = Task.objects.get(pk=id)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_task.status, STATUS.done)

    def test_should_return_404_when_calling_put_for_task_not_owned_by_current_user(self):
        # given
        self.client.login(username='test', password='test')
        id = 4
        task = Task.objects.get(pk=id)
        self.assertEqual(task.status, STATUS.active)
        task.status = STATUS.done
        put_data = TaskSerializer(task).data

        # when
        response = self.client.put(
            path=reverse("api:task", kwargs={"version": "v1", "pk": id}),
            data=put_data
        )

        # then
        self.assertEqual(response.status_code, 404)

    def test_should_update_task_using_patch_method(self):
        # given
        self.client.login(username='test', password='test')
        id = 1
        task = Task.objects.get(pk=id)
        self.assertEqual(task.status, STATUS.active)
        task.status = STATUS.done
        patch_data = {'status': 'done'}

        # when
        response = self.client.patch(
            path=reverse("api:task", kwargs={"version": "v1", "pk": id}),
            data=patch_data
        )
        updated_task = Task.objects.get(pk=id)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_task.status, STATUS.done)

    def test_should_return_404_when_calling_patch_for_task_not_owned_by_current_user(self):
        # given
        self.client.login(username='test', password='test')
        id = 4
        task = Task.objects.get(pk=id)
        self.assertEqual(task.status, STATUS.active)
        task.status = STATUS.done
        patch_data = {'status': 'done'}

        # when
        response = self.client.patch(
            path=reverse("api:task", kwargs={"version": "v1", "pk": id}),
            data=patch_data
        )

        # then
        self.assertEqual(response.status_code, 404)

    def test_should_delete_task(self):
        # given
        self.client.login(username='test', password='test')
        id = 1

        # when
        response = self.client.delete(
            path=reverse("api:task", kwargs={"version": "v1", "pk": id}),
        )

        # then
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=id)
        self.assertEqual(response.status_code, 204)

    def test_should_return_404_when_deleting_task_not_owned_by_current_user(self):
        # given
        self.client.login(username='test', password='test')
        id = 4

        # when
        response = self.client.delete(
            path=reverse("api:task", kwargs={"version": "v1", "pk": id}),
        )

        # then
        self.assertEqual(response.status_code, 404)

from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import Task
# Create your tests here.


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='a@example.com', password='pass1234')
        self.other = User.objects.create_user(email='b@example.com', password='pass1234')
        Task.objects.create(user=self.other, title='Other task')

    def test_create_task_via_view(self):
        self.client.login(email='a@example.com', password='pass1234')
        resp = self.client.post(reverse('todo:task-create'), {
            'title': 'My task',
            'description': 'desc',
            'priority': 'M',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 1)

    def test_cannot_toggle_other_user_task(self):
        t = Task.objects.create(user=self.other, title='Other2')
        self.client.login(email='a@example.com', password='pass1234')
        resp = self.client.post(reverse('todo:task-toggle', args=[t.pk]))
        self.assertEqual(resp.status_code, 404)

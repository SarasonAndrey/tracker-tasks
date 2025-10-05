from django.test import TestCase
from rest_framework.test import APIClient
from .models import Employee, Task
from .serializers import TaskSerializer


class EmployeeTestCase(TestCase):
    """
    Тесты для модели Employee.
    """
    def setUp(self):
        self.client = APIClient()
        self.employee = Employee.objects.create(
            full_name="Иванов Иван",
            position="Разработчик"
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.full_name, "Иванов Иван")

class TaskTestCase(TestCase):
    """
    Тесты для модели Task.
    """
    def setUp(self):
        self.employee = Employee.objects.create(
            full_name="Петров Пётр",
            position="Менеджер"
        )
        self.task = Task.objects.create(
            title="Написать отчет",
            assignee=self.employee,
            due_date="2025-01-01",
            status="pending"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Написать отчет")

    def test_task_due_date_validation(self):
        serializer = TaskSerializer(data={
            'title': 'Test Task',
            'assignee': self.employee.id,
            'due_date': '2020-01-01',  # Прошлое
            'status': 'pending'
        })
        self.assertFalse(serializer.is_valid())
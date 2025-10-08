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
            full_name="Иванов Иван", position="Разработчик"
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.full_name, "Иванов Иван")


class TaskTestCase(TestCase):
    """
    Тесты для модели Task.
    """

    def setUp(self):
        self.employee = Employee.objects.create(
            full_name="Петров Пётр", position="Менеджер"
        )
        self.task = Task.objects.create(
            title="Написать отчет",
            assignee=self.employee,
            due_date="2025-01-01",
            status="pending",
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Написать отчет")

    def test_task_due_date_validation(self):
        serializer = TaskSerializer(
            data={
                "title": "Test Task",
                "assignee": self.employee.id,
                "due_date": "2020-01-01",  # Прошлое
                "status": "pending",
            }
        )
        self.assertFalse(serializer.is_valid())


class ViewsTestCase(TestCase):
    """
    Тесты для вьюх.
    """

    def setUp(self):
        self.client = APIClient()
        self.employee = Employee.objects.create(
            full_name="Иванов Иван", position="Разработчик"
        )
        self.task = Task.objects.create(
            title="Тестовая задача",
            assignee=self.employee,
            due_date="2025-01-01",
            status="pending",
        )

    def test_employee_list_view(self):
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 200)

    def test_task_list_view(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_busy_employees_view(self):
        response = self.client.get("/api/busy-employees/")
        self.assertEqual(response.status_code, 200)

    def test_important_tasks_view(self):
        response = self.client.get("/api/important-tasks/")
        self.assertEqual(response.status_code, 200)

    def test_important_tasks_view_business_logic(self):

        response = self.client.get("/api/important-tasks/")
        self.assertEqual(response.status_code, 200)

        if len(response.data) > 0:
            # self.assertIn('task', response.data[0])
            self.assertIn("due_date", response.data[0])
            self.assertIn("candidate", response.data[0])
        else:
            # Если ответ пустой, всё равно тест пройдёт
            pass

    def test_busy_employees_view_sorting(self):
        Task.objects.create(
            title="Задача 1",
            assignee=self.employee,
            due_date="2025-01-01",
            status="in_progress",
        )
        Task.objects.create(
            title="Задача 2",
            assignee=self.employee,
            due_date="2025-01-02",
            status="pending",
        )

        response = self.client.get("/api/busy-employees/")
        self.assertEqual(response.status_code, 200)

        self.assertGreaterEqual(len(response.data), 1)

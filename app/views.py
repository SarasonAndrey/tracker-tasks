from django.db.models import Count, Q
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Employee, Task
from .serializers import EmployeeSerializer, TaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Employee.
    Обеспечивает CRUD-операции.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Task.
    Обеспечивает CRUD-операции.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BusyEmployeesView(generics.ListAPIView):
    """
    Возвращает список сотрудников, отсортированный по количеству активных задач.
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.annotate(
            task_count=Count(
                "task", filter=Q(task__status__in=["pending", "in_progress"])
            )
        ).order_by("-task_count")


class ImportantTasksView(APIView):
    """
    Возвращает важные задачи и кандидатов для их выполнения.
    """

    def get(self, request):

        dependent_tasks = Task.objects.filter(
            parent_task__isnull=False, status="in_progress"
        ).values_list("parent_task_id", flat=True)

        important_tasks = Task.objects.filter(
            id__in=dependent_tasks, status__in=["pending", "completed"]
        ).exclude(status="completed")

        result = []
        for task in important_tasks:

            least_loaded = (
                Employee.objects.annotate(
                    task_count=Count(
                        "task", filter=Q(task__status__in=["pending", "in_progress"])
                    )
                )
                .order_by("task_count")
                .first()
            )

            parent_assignee = task.parent_task.assignee if task.parent_task else None

            candidate = parent_assignee or least_loaded

            if candidate:
                result.append(
                    {
                        "task": task.title,
                        "due_date": task.due_date,
                        "candidate": candidate.full_name,
                    }
                )

        return Response(result)

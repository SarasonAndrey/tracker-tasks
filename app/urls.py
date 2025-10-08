from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BusyEmployeesView, EmployeeViewSet, ImportantTasksView, TaskViewSet

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("busy-employees/", BusyEmployeesView.as_view()),
    path("important-tasks/", ImportantTasksView.as_view()),
] + router.urls

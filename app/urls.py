from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BusyEmployeesView, EmployeeViewSet, ImportantTasksView, TaskViewSet

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/busy-employees/", BusyEmployeesView.as_view()),
    path("api/important-tasks/", ImportantTasksView.as_view()),
]

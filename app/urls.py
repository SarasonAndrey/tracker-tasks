from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, TaskViewSet, BusyEmployeesView, ImportantTasksView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/busy-employees/', BusyEmployeesView.as_view()),
    path('api/important-tasks/', ImportantTasksView.as_view()),
]
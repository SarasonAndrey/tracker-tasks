from django.contrib import admin

from .models import Employee, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "position"]
    search_fields = ["full_name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "assignee", "status", "due_date"]
    list_filter = ["status", "due_date"]
    search_fields = ["title"]

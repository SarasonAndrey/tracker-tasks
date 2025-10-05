from rest_framework import serializers
from .models import Employee, Task
from datetime import date


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Срок не может быть в прошлом.")
        return value

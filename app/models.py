from django.db import models


class Employee(models.Model):
    """
    Модель сотрудника.
    Содержит информацию о ФИО и должности.
    """

    full_name = models.CharField(
        max_length=255, verbose_name="ФИО", help_text="Введите полное имя сотрудника"
    )
    position = models.CharField(
        max_length=255,
        verbose_name="Должность",
        help_text="Введите должность сотрудника",
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Task(models.Model):
    """
    Модель задачи.
    Содержит название, статус, исполнителя, срок и зависимости.
    """

    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("in_progress", "В работе"),
        ("completed", "Выполнена"),
    ]

    title = models.CharField(
        max_length=255, verbose_name="Наименование", help_text="Введите название задачи"
    )
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Родительская задача",
        help_text="Задача, от которой зависит текущая",
    )
    assignee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Исполнитель",
        help_text="Сотрудник, которому назначена задача",
    )
    due_date = models.DateField(verbose_name="Срок", help_text="Дата окончания задачи")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

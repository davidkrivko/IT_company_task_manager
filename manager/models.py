from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.position}({self.username})"


class Task(models.Model):
    PRIORITY_LEVEL_CHOICES = (
        "high priority",
        "medium priority",
        "low priority",
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=15,
        choices=PRIORITY_LEVEL_CHOICES,
        default="medium priority"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL)
    assignees = models.ManyToManyField(Worker)

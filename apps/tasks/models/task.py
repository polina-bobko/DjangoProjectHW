from django.db import models

from .base import TimeStampedModel, UUIDv7Model


class Status(models.TextChoices):
    NEW = "new", "New"
    IN_PROGRESS = "in_progress", "In progress"
    PENDING = "pending", "Pending"
    BLOCKED = "blocked", "Blocked"
    DONE = "done", "Done"


class Task(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255,unique_for_date='created_at')
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(
        "Category",
        blank=True,
        related_name="tasks",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
    )
    deadline = models.DateTimeField()

    class Meta:
        db_table = "task_manager_task"
        ordering = ["deadline"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f'Task {self.title}'

    def __repr__(self):
        return (f'<Task(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})>')
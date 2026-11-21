from django.db import models

from .base import TimeStampedModel, UUIDv7Model
from .task import Task, Status


class SubTask(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
    )
    deadline = models.DateTimeField()

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ["deadline"]
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"

    def __str__(self):
        return f'Subtask {self.title}'

    def __repr__(self):
        return (f'SubTask(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})')

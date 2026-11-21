from django.db import models

from .base import TimeStampedModel, UUIDv7Model


class Status(models.TextChoices):
    NEW = "new", "New"
    IN_PROGRESS = "in_progress", "In progress"
    PENDING = "pending", "Pending"
    BLOCKED = "blocked", "Blocked"
    DONE = "done", "Done"


class Task(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255, unique=True, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    categories = models.ManyToManyField(
        "Category",
        blank=True,
        related_name="tasks",
        verbose_name="Категории задачи",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус задачи",
    )
    deadline = models.DateTimeField(verbose_name="Дата и время дедлайна")

    class Meta:
        db_table = 'task_manager_task'
        ordering = ('-created_at',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            models.UniqueConstraint('title', 'created_at',
                                    name='unique_title_by_creation_date',
                                    violation_error_message='Такая задача уже существует')
        ]

    def __str__(self):
        return self.title

    def __repr__(self):
        return (f'<Task(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})>')
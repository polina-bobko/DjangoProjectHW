from django.db import models

from .base import TimeStampedModel, UUIDv7Model
from .task import Task, Status
from django.conf import settings

class SubTask(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255, unique=True, verbose_name="Название подзадачи")
    description = models.TextField(blank=True, verbose_name="Описание подзадачи")
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name="Основная задача",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус подзадачи",
    )
    deadline = models.DateTimeField(verbose_name="Дата и время дедлайна")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name="Владелец подзадачи",
    )

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ('-created_at',)
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        constraints = [models.UniqueConstraint('title', 'created_at',
                                               name='unique_subtask_title_by_creation_date',
                                               violation_error_message='Такая сабтаска уже существует')]

    def __str__(self):
        return self.title

    def __repr__(self):
        return (f'SubTask(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})')

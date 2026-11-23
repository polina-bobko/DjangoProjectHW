from django.db import models

from .base import UUIDv7Model

from django.utils import timezone
from apps.tasks.managers import CategorySoftDeleteManager


class Category(UUIDv7Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата удаления категории"
    )

    objects = CategorySoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_category_name',
                                               violation_error_message='Such a Category already exists!')]

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(
            using=using,
            update_fields=["deleted_at"],
        )
    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name})>'
from django.db import models

from .base import UUIDv7Model


class Category(UUIDv7Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_category_name',
                                               violation_error_message='Such a Category already exists!')]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name})>'

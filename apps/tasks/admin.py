from django.contrib import admin

from .models import Category, Task, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "created_at", "deadline")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    filter_horizontal = ("categories",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "task",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "created_at", "deadline")
    search_fields = ("title", "description", "task__title")
    ordering = ("-created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
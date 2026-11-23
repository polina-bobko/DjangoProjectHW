from django.contrib import admin

from .models import Category, Task, SubTask
from .models.task import Status


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "short_title",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "created_at", "deadline")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    filter_horizontal = ("categories",)

    inlines = [SubTaskInline]

    @admin.display(description="Название задачи")
    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title


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

    @admin.action(description="Mark selected subtasks as Done")
    def mark_as_done(self, request, queryset):
        updated_count = queryset.update(status=Status.DONE)

        self.message_user(
            request,
            f"{updated_count} subtasks marked as Done."
        )

    actions = [mark_as_done]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "show_is_deleted",
        "deleted_at",
    )

    search_fields = ("name",)

    ordering = ("-name",)

    list_filter = (
        ("deleted_at", admin.EmptyFieldListFilter),
    )

    readonly_fields = (
        "is_deleted",
        "deleted_at",
    )

    @admin.display(
        boolean=True,
        description="Deleted?",
    )
    def show_is_deleted(self, category):
        return category.is_deleted

    def get_queryset(self, request):
        return Category.all_objects.all().order_by("-name")

    def delete_queryset(self, request, queryset):
        for category in queryset:
            category.delete()
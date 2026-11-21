
import os
from datetime import timedelta

import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)
django.setup()

from django.utils import timezone
from apps.tasks.models import Task, SubTask
from apps.tasks.models.task import Status


def create_records():
    print("\n=== CREATE ===")

    task = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status=Status.NEW,
        deadline=timezone.now() + timedelta(days=3),
    )

    subtasks = SubTask.objects.bulk_create([
        SubTask(
            title="Gather information",
            description="Find necessary information for the presentation",
            task=task,
            status=Status.NEW,
            deadline=timezone.now() + timedelta(days=2),
        ),
        SubTask(
            title="Create slides",
            description="Create presentation slides",
            task=task,
            status=Status.NEW,
            deadline=timezone.now() + timedelta(days=1),
        ),
        SubTask(
            title="Review presentation",
            description="Review and check presentation materials",
            task=task,
            status=Status.DONE,
            deadline=timezone.now() - timedelta(days=1),
        ),
    ])

    print(f"Created task: {task.title}")

    for subtask in subtasks:
        print(f"Created subtask: {subtask.title}")

def read_records():
    print("\n=== READ ===")

    print("Tasks with status New:")
    for task in Task.objects.filter(status=Status.NEW):
        print(f"- {task.title}")

    print("\nOverdue subtasks with status Done:")
    for subtask in SubTask.objects.filter(
        status=Status.DONE,
        deadline__lt=timezone.now(),
    ):
        print(f"- {subtask.title}")


def update_records():
    print("\n=== UPDATE ===")

    task = Task.objects.get(title="Prepare presentation")

    Task.objects.filter(pk=task.pk).update(
        status=Status.IN_PROGRESS
    )
    print("Task status changed to In progress")

    SubTask.objects.filter(
        task=task,
        title="Gather information",
    ).update(
        deadline=timezone.now() - timedelta(days=2)
    )
    print("Gather information deadline changed to 2 days ago")

    SubTask.objects.filter(
        task=task,
        title="Create slides",
    ).update(
        description="Create and format presentation slides"
    )
    print("Create slides description updated")

    task.refresh_from_db()
    print(f"Current task status: {task.get_status_display()}")

    for subtask in task.subtasks.all():
        print(
            f"{subtask.title}: "
            f"deadline={subtask.deadline}, "
            f"description={subtask.description}"
        )


def delete_records():
    print("\n=== DELETE ===")

    task = Task.objects.get(title="Prepare presentation")
    subtask_count = task.subtasks.count()

    deleted_count, details = task.delete()

    print(f"Related subtasks before deletion: {subtask_count}")
    print(f"Total deleted objects: {deleted_count}")
    print(f"Deletion details: {details}")

    print(
        "Task still exists:",
        Task.objects.filter(
            title="Prepare presentation"
        ).exists()
    )


if __name__ == "__main__":
    create_records()
    read_records()
    update_records()
    delete_records()
    #pass
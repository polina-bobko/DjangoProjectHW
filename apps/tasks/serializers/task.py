from django.utils import timezone
from rest_framework import serializers

from apps.tasks.models import Task
from .subtask import SubTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "subtasks",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
        ]
        read_only_fields = ["id"]

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Deadline cannot be in the past!"
            )

        return value
from rest_framework import serializers
from apps.tasks.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            "id",
            "task",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "updated_at",
            "owner",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "owner",
        ]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            "id",
            "task",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "updated_at",
            "owner",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "owner",
        ]

    def validate_task(self, value):
        if value.owner_id != self.context["request"].user.pk:
            raise serializers.ValidationError(
                "You can only assign subtasks to your own tasks."
            )
        return value
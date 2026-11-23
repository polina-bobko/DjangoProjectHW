from rest_framework import serializers
from apps.tasks.models import Category
from .task import TaskDetailSerializer


class CategorySerializer(serializers.ModelSerializer):

    tasks = TaskDetailSerializer(
        many=True,
        read_only=True,
    )

    is_deleted = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "tasks",
            "is_deleted",
            "deleted_at",
        ]

        read_only_fields = [
            "id",
            "tasks",
            "is_deleted",
            "deleted_at",
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):

    is_deleted = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "is_deleted",
            "deleted_at",
        ]

        read_only_fields = [
            "id",
            "is_deleted",
            "deleted_at",
        ]

        extra_kwargs = {
            "name": {"validators": []}
        }

    def create(self, validated_data):
        name = validated_data.get("name")

        if Category.all_objects.filter(name=name).exists():
            raise serializers.ValidationError({
                "name": "This category name already exists."
            })

        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name")

        if name is not None:
            if Category.all_objects.filter(
                name=name
            ).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError({
                    "name": "This category name already exists."
                })

        return super().update(instance, validated_data)
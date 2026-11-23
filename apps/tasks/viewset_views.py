from django.db.models import Count

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.tasks.models import Category

from apps.tasks.serializers import (
    CategorySerializer,
    CategoryCreateSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.prefetch_related(
        "tasks",
        "tasks__subtasks",
    )

    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action in (
            "create",
            "update",
            "partial_update",
        ):
            return CategoryCreateSerializer

        return CategorySerializer

    @action(
        detail=False,
        methods=["get"],
        url_name="count",
        url_path="count",
    )
    def count_tasks(self, request):
        categories = self.get_queryset().annotate(
            tasks_count=Count("tasks", distinct=True)
        )

        page = self.paginate_queryset(categories)

        if page is not None:
            data = [
                {
                    "id": category.id,
                    "name": category.name,
                    "tasks_count": category.tasks_count,
                }
                for category in page
            ]

            return self.get_paginated_response(data)

        return Response(
            list(categories.values(
                "id",
                "name",
                "tasks_count",
            )),
            status=status.HTTP_200_OK,
        )
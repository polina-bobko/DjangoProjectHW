from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import SubTask
from apps.tasks.models.task import Status
from .serializers import SubTaskSerializer, SubTaskCreateSerializer
from .paginators import SubTaskPaginator


class SubTaskListCreateView(APIView):

    def get(self, request):
        subtasks = SubTask.objects.select_related("task").all()

        filters = {}

        # Фильтр по названию главной задачи
        if task := request.query_params.get("task"):
            filters["task__title__icontains"] = task.strip()

        # Фильтр по статусу подзадачи
        if subtask_status := request.query_params.get("status"):
            subtask_status = subtask_status.strip().lower()

            valid_statuses = [choice.value for choice in Status]

            if subtask_status not in valid_statuses:
                return Response(
                    {"error": "Invalid subtask status"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters["status"] = subtask_status

        # Применяем фильтры и сортировку
        subtasks = subtasks.filter(**filters).order_by(
            "-created_at", "-id"
        )

        # Пагинация
        paginator = SubTaskPaginator()
        page = paginator.paginate_queryset(subtasks, request)

        if page is not None:
            serializer = SubTaskSerializer(page, many=True)
            return paginator.get_paginated_response(
                serializer.data
            )

        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = SubTaskCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubTaskDetailUpdateDeleteView(APIView):

    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskSerializer(subtask)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, partial=False):
        subtask = get_object_or_404(SubTask, pk=pk)

        serializer = SubTaskCreateSerializer(
            subtask,
            data=request.data,
            partial=partial
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        return self.put(request, pk, partial=True)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
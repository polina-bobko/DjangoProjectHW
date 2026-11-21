from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .models.task import Status
from .serializers import TaskSerializer


# Задание 1: создание задачи
@api_view(["POST"])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


# Задание 2: получение всех задач
@api_view(["GET"])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


# Задание 2: получение задачи по UUID
@api_view(["GET"])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(task)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


# Задание 3: статистика задач
@api_view(["GET"])
def task_statistics(request):
    total_tasks = Task.objects.count()

    status_counts = (
        Task.objects
        .values("status")
        .annotate(count=Count("id"))
    )

    tasks_by_status = {
        choice.value: 0
        for choice in Status
    }

    for item in status_counts:
        tasks_by_status[item["status"]] = item["count"]

    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now()
    ).exclude(
        status=Status.DONE
    ).count()

    return Response({
        "total_tasks": total_tasks,
        "tasks_by_status": tasks_by_status,
        "overdue_tasks": overdue_tasks,
    })
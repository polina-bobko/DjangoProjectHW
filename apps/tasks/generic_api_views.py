from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.tasks.models import Task, SubTask

from .filters import TaskFilter

from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)

from .paginators import TaskPaginator, SubTaskPaginator


# Tasks: получение списка и создание
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.prefetch_related(
        "categories", "subtasks"
    ).all()

    serializer_class = TaskSerializer
    pagination_class = TaskPaginator

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = TaskFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at", "-id"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer

        return TaskSerializer


# Tasks: получение, обновление и удаление
class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.prefetch_related(
        "categories", "subtasks"
    ).all()

    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskDetailSerializer

        if self.request.method in ("PUT", "PATCH"):
            return TaskCreateSerializer

        return TaskSerializer


# SubTasks: получение списка и создание
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.select_related("task").all()

    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPaginator

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ["status", "deadline"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at", "-id"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer

        return SubTaskSerializer


# SubTasks: получение, обновление и удаление
class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.select_related("task").all()

    serializer_class = SubTaskSerializer

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return SubTaskCreateSerializer

        return SubTaskSerializer
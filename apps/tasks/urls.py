from django.urls import path

# from .views import (
#     create_task,
#     task_list,
#     task_detail,
#     task_statistics,
# )

from .generic_api_views import CurrentUserTasksView
from . import views as tasks_

from .generic_api_views import (
    TaskListCreateView,
    TaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

# from .api_views import (
#     SubTaskListCreateView,
#     SubTaskDetailUpdateDeleteView,
# )

# urlpatterns = [
#     path(
#         "tasks/create/",
#         create_task,
#         name="task-create"
#     ),
#     path(
#         "tasks/",
#         task_list,
#         name="task-list"
#     ),
#     path(
#         "tasks/statistics/",
#         task_statistics,
#         name="task-statistics"
#     ),
#     path(
#         "tasks/<uuid:pk>/",
#         task_detail,
#         name="task-detail"
#     ),
#     path(
#         "subtasks/",
#         SubTaskListCreateView.as_view(),
#         name="subtask-list-create"
#     ),
#     path(
#         "subtasks/<uuid:pk>/",
#         SubTaskDetailUpdateDeleteView.as_view(),
#         name="subtask-detail-update-delete"
#     ),
# ]

urlpatterns = [
    path(
        "tasks/statistics/",
        tasks_.task_statistics,
        name="tasks-statistics",
    ),
    path(
        "tasks/",
        TaskListCreateView.as_view(),
        name="task-get-all-or-create",
    ),
    path(
        "tasks/<uuid:pk>/",
        TaskDetailUpdateDeleteView.as_view(),
        name="task-get-one-or-update-or-delete",
    ),
    path(
        "subtasks/",
        SubTaskListCreateView.as_view(),
        name="subtask-get-all-or-create",
    ),
    path(
        "subtasks/<uuid:pk>/",
        SubTaskDetailUpdateDeleteView.as_view(),
        name="subtask-get-update-delete",
    ),
    path(
        "my/tasks/",
        CurrentUserTasksView.as_view(),
        name="owner-get-all-tasks",
    ),
]
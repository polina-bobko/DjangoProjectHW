from rest_framework.pagination import CursorPagination


class CommonPaginator(CursorPagination):
    page_size = 6
    ordering = "id"
    page_size_query_param = None
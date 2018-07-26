from rest_framework.pagination import PageNumberPagination


class SnippetListPagination(PageNumberPagination):
    page_size = 3

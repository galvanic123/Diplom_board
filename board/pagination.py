from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.pagination import PageNumberPagination


class ADSPagination(PageNumberPagination):
    django_paginator_class = DjangoPaginator
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        if not queryset.ordered:
            queryset = queryset.order_by('-created_at')
        return super().paginate_queryset(queryset, request, view)
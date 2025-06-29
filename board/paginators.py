from rest_framework.pagination import PageNumberPagination


class ADSPagination(PageNumberPagination):
    """Вывод списка до 6 объявлений и отзывов"""

    page_size = 4
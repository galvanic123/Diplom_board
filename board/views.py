from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import ADSPagination
from board.filters import AdvertisementFilter
from board.models import Advertisement, Comment

from board.serializers import (
    AdvertisementRetrieveSerializer,
    AdvertisementSerializer,
    CommentSerializer,
)
from users.permissions import IsModer, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для получения списка"
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для получения конкретной"
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Контроллер для создания"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для обновления информации"
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для частичного изменения информации"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Контроллер для удаления"),
)
class AdvertisementViewSet(viewsets.ModelViewSet):
    """CRUD объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    pagination_class = ADSPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = AdvertisementFilter
    filterset_fields = (
        "category__slug",
        "owner",
        "title",
        "created_at",
    )
    search_fields = ("title",)
    ordering_fields = ("created_at",)

    def perform_create(self, serializer):
        # advertisement = serializer.save()
        # advertisement.owner = self.request.user
        # advertisement.save()
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action == "retrieve":
            return AdvertisementRetrieveSerializer
        return AdvertisementSerializer

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in "retrieve":
            self.permission_classes = [IsAuthenticated | IsModer | IsOwner]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwner | IsModer]

        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class CommentCreateAPIView(generics.CreateAPIView):
    """Создание отзыва."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, advertisement=serializer.validated_data['advertisement'])
        # comment = serializer.save()
        # comment.owner = self.request.user
        # comment.save()


class CommentListAPIView(generics.ListAPIView):
    """Список отзывов."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = ADSPagination
    permission_classes = [AllowAny]

# class CommentDetailView(generics.ListAPIView):
#     """Отзыв."""
#
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]

class CommentUpdateAPIView(generics.UpdateAPIView):
    """Редактирование отзыва."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class CommentDestroyAPIView(generics.DestroyAPIView):
    """Удаление отзыва."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

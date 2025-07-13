from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.apps import BoardConfig
from board.views import (
    AdvertisementViewSet,
    CommentCreateAPIView,
    CommentDestroyAPIView,
    CommentListAPIView,
    CommentUpdateAPIView,
)

app_name = BoardConfig.name


router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
    path("comments/create/", CommentCreateAPIView.as_view(), name="comment_create"),
    path(
        "comment/<int:pk>/update", CommentUpdateAPIView.as_view(), name="comment_update"
    ),
    path("comment_list/", CommentListAPIView.as_view(), name="comment_list"),
    # path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path(
        "comment/delete/<int:pk>",
        CommentDestroyAPIView.as_view(),
        name="comment_delete",
    ),
] + router.urls

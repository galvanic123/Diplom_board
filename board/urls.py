from django.urls import path
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
router.register(r"advertisement", AdvertisementViewSet, basename="advertisement")

urlpatterns = [
    path("comment_create/", CommentCreateAPIView.as_view(), name="comment_create"),
    path(
        "comment/<int:pk>/update", CommentUpdateAPIView.as_view(), name="comment_update"
    ),
    path("comment_list/", CommentListAPIView.as_view(), name="comment_list"),
    path(
        "comment/<int:pk>/delete",
        CommentDestroyAPIView.as_view(),
        name="comment_delete",
    ),
] + router.urls

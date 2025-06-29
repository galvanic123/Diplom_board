from django.urls import path
from rest_framework.routers import DefaultRouter

from board.apps import BoardConfig
from board.views import (AdvertisementViewSet, CommentCreateAPIView,
                                 CommentDestroyAPIView, CommentListAPIView,
                                 CommentUpdateAPIView)

app_name = BoardConfig.name


router = DefaultRouter()
router.register(r"announcement", AdvertisementViewSet, basename="announcement")

urlpatterns = [
    path("review_create/", CommentCreateAPIView.as_view(), name="review_create"),
    path("review/<int:pk>/update", CommentUpdateAPIView.as_view(), name="review_update"),
    path("review_list/", CommentListAPIView.as_view(), name="review_list"),
    path(
        "review/<int:pk>/delete", CommentDestroyAPIView.as_view(), name="review_delete"
    ),
] + router.urls
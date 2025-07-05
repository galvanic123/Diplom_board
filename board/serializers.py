from rest_framework import serializers

from .models import Advertisement, Comment
from .validators.validators import (
    ForbiddenWordValidator,
    RepeatAdvertisementValidator,
    price_zero_validator,
)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""

    class Meta:
        model = Comment
        fields = ("id", "text", "rating", "created_at", "owner")
        validators = [ForbiddenWordValidator(comment_text="text")]


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления"""

    price = serializers.IntegerField(validators=(price_zero_validator,))
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "price",
            "description",
            "image",
            "created_at",
            "owner",
            "average_rating",
        )
        validators = [
            ForbiddenWordValidator(
                advertisement_title="title", advertisement_description="description"
            ),
            RepeatAdvertisementValidator(
                title="title", description="description", price="price"
            ),
        ]

    def get_average_rating(self, obj):
        # Вариант 1: Если related_name не указан (используем _set)
        comments = obj.comments.all()  # Или comment_set, в зависимости от вашей модели

        # Вариант 2: Если указан related_name='comments'
        # comments = obj.comments.all()

        if comments.exists():
            return round(
                sum(comment.rating for comment in comments) / comments.count(), 1
            )
        return 0


class AdvertisementRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного объявления"""

    advertisement_reviews = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = (
            "id",
            "title",
            "price",
            "description",
            "image",
            "created_at",
            "owner",
            "advertisement_comments",
        )

from rest_framework import serializers

from .models import Advertisement, Comment
from .validators.validators import (ForbiddenWordValidator,
                                    RepeatAdvertisementValidator,
                                    price_zero_validator)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""

    class Meta:
        model = Comment
        fields = ("id", "text", "rating", "created_at", "announcement", "owner")
        validators = [ForbiddenWordValidator(review_text="text")]


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
        """Получаем общий рейтинг для данного объявления"""
        reviews = obj.advertisement_reviews.all()

        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return round(average_rating, 2)
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
            "advertisement_reviews",
        )

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
        fields = ("id", "text", "rating", "created_at", "owner", "advertisement")
        read_only_fields = ["owner"]
        extra_kwargs = {
            'owner': {'read_only': True}
        }
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
            'category',
        )
        read_only_fields = ['owner']

        def create(self, validated_data):
            validated_data["owner"] = self.context["request"].user
            return super().create(validated_data)

        validators = [
            ForbiddenWordValidator(
                advertisement_title="title", advertisement_description="description"
            ),
            RepeatAdvertisementValidator(
                title="title", description="description", price="price"
            ),
        ]

    def get_average_rating(self, obj):

        comments = obj.comments.all()

        if comments.exists():
            return round(
                sum(comment.rating for comment in comments) / comments.count(), 1
            )
        return 0


class AdvertisementRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного объявления"""

    advertisement_comments = CommentSerializer(many=True, read_only=True)

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
            'category',
        )

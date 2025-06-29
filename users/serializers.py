from rest_framework import serializers

from board.models import Comment
from board.paginators import ADSPagination
from board.serializers import AdvertisementSerializer, CommentSerializer

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля"""

    class Meta:
        model = User
        fields = "__all__"


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор для владельца профиля"""

    advertisements = AdvertisementSerializer(many=True, read_only=True)
    author_reviews = CommentSerializer(many=True, read_only=True)
    received_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "advertisements",
            "author_reviews",
            "received_reviews",
            "average_rating",
        )

    def get_received_reviews(self, obj):
        """Получаем оставленные отзывы"""
        advertisements = obj.advertisements.all()
        reviews = Comment.objects.filter(advertisement__in=advertisements)

        paginator = ADSPagination()
        paginated_reviews = paginator.paginate_queryset(
            reviews, self.context["request"]
        )

        return CommentSerializer(paginated_reviews, many=True).data

    def get_average_rating(self, obj):
        """Получаем общий рейтинг"""
        advertisements = obj.advertisements.all()
        reviews = Comment.objects.filter(advertisement__in=advertisements)

        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return round(average_rating, 2)
        return 0


class ProfileOwnerAdSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей, не являющихся владельцами профиля"""

    advertisements = AdvertisementSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    overall_rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "phone_number",
            "avatar",
            "advertisements",
            "comments",
            "overall_rating",
        )

    def get_reviews(self, obj):
        """Получаем оставленные отзывы"""
        advertisements = obj.advertisements.all()
        reviews = Comment.objects.filter(advertisement__in=advertisements)

        paginator = ADSPagination()
        paginated_reviews = paginator.paginate_queryset(
            reviews, self.context["request"]
        )
        return CommentSerializer(paginated_reviews, many=True).data

    def get_overall_rating(self, obj):
        """Получаем общий рейтинг"""
        advertisements = obj.advertisements.all()
        reviews = Comment.objects.filter(advertisement__in=advertisements)

        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            return round(average_rating, 2)
        return 0
